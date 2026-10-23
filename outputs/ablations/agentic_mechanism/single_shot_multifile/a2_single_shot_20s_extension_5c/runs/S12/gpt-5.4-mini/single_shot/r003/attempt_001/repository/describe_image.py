import os
from typing import Optional

from openai import OpenAI

from vision_client import build_openai_client, image_input_from_path_or_bytes
from vision_models import DescriptionResult, normalize_description_result

MODEL_ID = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")


def describe_image(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None, client: Optional[OpenAI] = None) -> DescriptionResult:
    client = client or build_openai_client()
    image_input = image_input_from_path_or_bytes(image_path=image_path, image_bytes=image_bytes)
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {
                "role": "system",
                "content": "Write a short, accurate, natural-language visual description of the image.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Describe this image in 1-3 sentences."},
                    {"type": "input_image", "image_url": image_input},
                ],
            },
        ],
        temperature=0.2,
    )
    return normalize_description_result(response.output_text)
