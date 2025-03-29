from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from typing import Optional
import asyncio
from vlm_qwen2b import process_image_and_text

app = FastAPI()


@app.post("/stream_process_image/")
async def stream_process_image(files: Optional[UploadFile] = File(None), text_prompt: str = Form(None)):
    """
    Streams the result from the VLM processing.
    """
    image_content = None
    if files:
        image_content = await files.read()

    return StreamingResponse(process_image_and_text(image_content, text_prompt), media_type="text/plain")


@app.get("/health")
async def health_check():
    return {"status": "ok"}