from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio
import io
from PIL import Image
from fastapi.responses import PlainTextResponse  # Import PlainTextResponse

from models.vlm_model import process_vlm

app = FastAPI()

# CORS configuration - adjust origins for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins - VERY permissive, restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/process_image/", response_class=PlainTextResponse)
async def process_image(files: List[UploadFile] = File(...), text_prompt: str = ""):
    """
    Processes an image using a VLM model based on the provided text prompt.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No image files provided.")

    try:
        contents = await files[0].read()
        # Verify its an image (optional, but good practice)
        try:
            img = Image.open(io.BytesIO(contents))
            img.verify()  # Verify that it is indeed an image
            img.close()  # Close the image after verification
        except Exception as e:
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

        # Call the VLM processing function
        result = process_vlm(contents, text_prompt)  # Pass the bytes, remove await

        if result is None:
            raise HTTPException(status_code=500, detail="VLM processing failed.")  # Handle VLM failure

        return result  # Return the Markdown result directly

    except HTTPException as http_ex:
        # Re-raise HTTPExceptions to preserve their status codes
        raise http_ex

    except Exception as e:
        print(f"Error during image processing: {e}")  # Log the error for debugging
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "ok"}