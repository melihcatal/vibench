import os
from typing import Any, Dict, Optional

from vision_client import build_openai_client, image_to_data_url
from vision_models import DescriptionResult

_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")


def describe_image(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None, image_url: Optional[str] = None) -> Dict[str, Any]:
    client = build_openai_client()
    data_url = image_to_data_url(image_path=image_path, image_bytes=image_bytes, image_url=image_url)
    prompt = "Write one short, natural visual description of this image."
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
        temperature=0.2,
    )
    text = getattr(response, "output_text", "") or ""
    return DescriptionResult(description=text.strip(), raw_text=text).to_dict()
