import ollama
from PIL import Image
import io
import os
from typing import Optional

# Determine device (CPU for Ollama)
device = "cpu"  # Ollama primarily targets CPU, but can use GPU if configured separately.
print(f"Using device: {device}")

# Define the model name (replace with your desired llama3:2b model from Ollama)
MODEL_NAME = "llama3:8b-instruct" # Make sure you have this model pulled using `ollama pull llama3:8b-instruct`

def load_model():
    """
    Loads the Llama3 model through Ollama.  No explicit loading needed as Ollama handles it on demand.

    Returns:
        A boolean indicating success.  Ollama dynamically loads the model when needed,
        so this function primarily checks if Ollama itself is running.
    """
    try:
        # Attempt a simple request to Ollama to check its availability.
        ollama.pull(MODEL_NAME)
        return True
    except Exception as e:
        print(f"Error connecting to Ollama or loading model: {e}")
        print("Make sure Ollama is running and the model is pulled.")
        return False


# Load model (run this only once when the backend starts)
model_loaded = load_model()


def process_image_and_text(
    image_bytes: Optional[bytes] = None, text_prompt: Optional[str] = None, max_new_tokens: int = 500
):
    """
    Processes the image and text prompt using the Llama3 model via Ollama.

    Args:
        image_bytes: Bytes of the image to process. If None, only the text prompt is used.
        text_prompt: Text prompt to guide the image understanding. If None, the image is processed without a text prompt.
        max_new_tokens: Maximum number of tokens to generate in the response.

    Returns:
        A generator that yields chunks of text from the model's output.
    """

    if not model_loaded:
        yield "Error: Llama3 model not loaded. Check Ollama is running and the model is pulled."
        return

    if not image_bytes and not text_prompt:
        yield "Error: No image or text provided."
        return

    prompt = ""
    images = []

    if image_bytes:
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # Ensure RGB
            image_bytes_for_ollama = io.BytesIO()
            image.save(image_bytes_for_ollama, format="PNG")  #Ollama requires PNG
            images = [image_bytes_for_ollama.getvalue()]
        except Exception as e:
            yield f"Error processing image: {e}"
            return

        if text_prompt:
            prompt = f"Image description: {text_prompt}"
        else:
            prompt = "Describe the image."
    else:
         prompt = text_prompt
         images = []  # Ensure images is an empty list if no image is provided

    try:
        # Call Ollama API
        stream = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
            images=images, # Pass the image bytes as a list, even with one image.
            stream=True,
            options={"num_predict": max_new_tokens}
        )

        # Stream the output
        for part in stream:
             yield part["response"]

    except Exception as e:
        yield f"Error during processing with Ollama: {e}"