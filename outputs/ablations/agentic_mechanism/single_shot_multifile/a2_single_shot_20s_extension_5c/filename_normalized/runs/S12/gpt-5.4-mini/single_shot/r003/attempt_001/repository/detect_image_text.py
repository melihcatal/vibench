import os
from typing import Optional

from openai import OpenAI

from vision_client import build_openai_client, image_input_from_path_or_bytes
from vision_models import OCRResult, normalize_ocr_result

MODEL_ID = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")


def detect_image_text(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None, client: Optional[OpenAI] = None) -> OCRResult:
    client = client or build_openai_client()
    image_input = image_input_from_path_or_bytes(image_path=image_path, image_bytes=image_bytes)
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {
                "role": "system",
                "content": "Extract all clearly visible text from the image. Preserve line breaks where helpful and return structured JSON.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Transcribe all visible text from this image."},
                    {"type": "input_image", "image_url": image_input},
                ],
            },
        ],
        temperature=0,
    )
    return normalize_ocr_result(response.output_text)
