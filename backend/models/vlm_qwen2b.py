from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch
from PIL import Image
import io
import os

# Determine device (CUDA if available, otherwise CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Define the cache directory in the same directory as this script
cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Weights")
os.makedirs(cache_dir, exist_ok=True)  # Ensure the directory exists
print(f"Using cache directory: {cache_dir}")


def load_model():
    """
    Loads the Qwen2-VL model and processor.

    Returns:
        A tuple containing the model and processor, or (None, None) if loading fails.
    """
    try:
        model = Qwen2VLForConditionalGeneration.from_pretrained(
            "Qwen/Qwen2-VL-2B-Instruct",
            torch_dtype="auto",
            cache_dir=cache_dir,  # Removed device_map
        )
        model = model.to(device)  # Move to device AFTER loading
        processor = AutoProcessor.from_pretrained(
            "Qwen/Qwen2-VL-2B-Instruct", cache_dir=cache_dir
        )

        print("Qwen2-VL model loaded successfully!")
        return model, processor
    except Exception as e:
        print(f"Error loading Qwen2-VL model: {e}")
        return None, None


# Load model and processor (run this only once when the backend starts)
model, processor = load_model()


def process_image_and_text(
    image_bytes: bytes = None, text_prompt: str = None, max_new_tokens: int = 500
):
    """
    Processes the image and text prompt using the Qwen2-VL model.

    Args:
        image_bytes: Bytes of the image to process.  If None, only the text prompt is used.
        text_prompt: Text prompt to guide the image understanding.  If None, the image is processed without a text prompt.
        max_new_tokens: Maximum number of tokens to generate in the response.

    Returns:
        A generator that yields chunks of text from the model's output.
    """

    if model is None or processor is None:
        yield "Error: Qwen2-VL model not loaded."
        return

    messages = []
    if image_bytes:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # Ensure RGB
        messages.append({"role": "user", "content": [{"type": "image", "image": image}]})
    if text_prompt:
        messages.append({"role": "user", "content": [{"type": "text", "text": text_prompt}]})

    if not messages:
        yield "Error: No image or text provided."
        return

    try:
        # Preparation for inference
        text = processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        if image_bytes:
            image_inputs, video_inputs = process_vision_info(messages)
            inputs = processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt",
            )

            inputs = inputs.to(device)  # Move to the determined device

        else:  # only text
            inputs = processor(
                text=[text], padding=True, return_tensors="pt"
            )
            inputs = inputs.to(device)  # Move to the determined device

        # Inference: Generation of the output
        generated_ids = model.generate(**inputs, max_new_tokens=max_new_tokens)
        generated_ids_trimmed = [
            out_ids[len(in_ids) :] for in_ids, out_ids in zip(
                inputs.input_ids, generated_ids)
        ]

        output_text = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0]  # Get the first element of the list

        # Stream the output (split into chunks)
        chunk_size = 50  # Adjust as needed
        for i in range(0, len(output_text), chunk_size):
            yield output_text[i:i + chunk_size]

    except Exception as e:
        yield f"Error during processing: {e}"