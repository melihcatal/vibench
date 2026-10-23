import os
from typing import Any, Dict, Optional

from vision_client import build_openai_client, image_to_data_url
from vision_models import OCRResult, normalize_text_lines

_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")


def detect_image_text(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None, image_url: Optional[str] = None) -> Dict[str, Any]:
    client = build_openai_client()
    data_url = image_to_data_url(image_path=image_path, image_bytes=image_bytes, image_url=image_url)
    prompt = "Read all visible text in this image. Preserve line breaks where helpful and return only the transcription."
    response = client.responses.create(
        model=_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": data_url},
                ],
            }
        ],
        temperature=0,
    )
    text = getattr(response, "output_text", "") or ""
    lines = normalize_text_lines(text)
    return OCRResult(text=text.strip(), lines=lines).to_dict()
