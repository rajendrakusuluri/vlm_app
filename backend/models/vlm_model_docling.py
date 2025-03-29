import torch
import os
from docling_core.types.doc import DoclingDocument
from docling_core.types.doc.document import DocTagsDocument
from transformers import AutoProcessor, AutoModelForVision2Seq
from transformers.image_utils import load_image
from io import BytesIO
from PIL import Image

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Global variables to store the model and processor (loaded once)
processor = None
model = None
model_loaded = False 

def determine_weights_dir():
    """Determines the weights directory based on the file path."""
    dir_path = os.path.dirname(os.path.abspath(__file__))  # Get absolute directory of the file
    weights_dir = os.path.join(os.path.dirname(os.path.dirname(dir_path)),'Weights')# Go one folder up
    print(weights_dir)
    return weights_dir

def download_model_weights( model_name="ds4sd/SmolDocling-256M-preview"):
    """Downloads the model weights and processor configuration to the directory one level above the file's directory."""
    weights_dir = determine_weights_dir()

    if not os.path.exists(weights_dir):
        os.makedirs(weights_dir)  # Create the directory if it doesn't exist
    
    try:
        AutoProcessor.from_pretrained(model_name, cache_dir=weights_dir)
        AutoModelForVision2Seq.from_pretrained(model_name, cache_dir=weights_dir)
        print(f"Model weights and processor downloaded to: {weights_dir}")
    except Exception as e:
        print(f"Error downloading model weights: {e}")
        raise  # Re-raise the exception to stop execution if the download fails


def load_model():
    """Loads the processor and model from the directory one level above the file's directory."""
    global processor, model, model_loaded
    weights_dir = determine_weights_dir()

    if not model_loaded:  # Only load if the model hasn't been loaded yet
        try:
            processor = AutoProcessor.from_pretrained("ds4sd/SmolDocling-256M-preview", cache_dir=weights_dir)
            model = AutoModelForVision2Seq.from_pretrained(
                "ds4sd/SmolDocling-256M-preview", cache_dir=weights_dir,
                torch_dtype=torch.bfloat16,
                _attn_implementation="flash_attention_2" if DEVICE == "cuda" else "eager",
            ).to(DEVICE)
            model.eval()  
            model_loaded = True  
            print("Model loaded successfully from: ", weights_dir)
        except Exception as e:
            print(f"Error loading model: {e}")
            raise


def process_vlm(image_data, text_prompt):
    """
    Processes an image using a VLM model to convert it to Docling format.

    Args:
        image_data (bytes): The byte data of the image.
        text_prompt (str): The text prompt to guide the VLM (e.g., "Convert this page to docling.").

    Returns:
        str: The Docling representation of the document.  Returns None if processing fails.
    """
    global processor, model

    # Load the model and processor if not already loaded
    try:
        load_model()
    except Exception as e:
        print(f"Failed to load model: {e}")
        return None

    try:
        # Load the image from bytes
        image = load_image(Image.open(BytesIO(image_data)))

        # Create input messages
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "text", "text": text_prompt}
                ]
            },
        ]

        # Prepare inputs
        prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
        inputs = processor(text=prompt, images=[image], return_tensors="pt")
        inputs = inputs.to(DEVICE)

        # Generate outputs
        with torch.no_grad():  # Disable gradient calculation during inference
            generated_ids = model.generate(**inputs, max_new_tokens=8192)

        prompt_length = inputs.input_ids.shape[1]
        trimmed_generated_ids = generated_ids[:, prompt_length:]
        doctags = processor.batch_decode(
            trimmed_generated_ids,
            skip_special_tokens=False,
        )[0].lstrip()

        # Populate document
        doctags_doc = DocTagsDocument.from_doctags_and_image_pairs([doctags], [image])

        # Create a docling document
        doc = DoclingDocument(name="Document")
        doc.load_from_doctags(doctags_doc)

        # Export as markdown
        return doc.export_to_markdown()

    except Exception as e:
        print(f"Error during VLM processing: {e}")
        return None # Or raise the exception again, depending on your error handling strategy