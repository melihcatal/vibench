from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

from vision_client import image_to_data_url
from vision_models import VisualDescription


OPENAI_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")


def describe_image(image_path: str, prompt: Optional[str] = None) -> VisualDescription:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    user_prompt = prompt or "Write a short, concrete description of this image in one sentence."
    data_url = image_to_data_url(image_path)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": user_prompt},
                    {"type": "input_image", "image_url": data_url},
                ],
            }
        ],
        max_output_tokens=80,
    )
    return VisualDescription(text=response.output_text.strip(), model=OPENAI_MODEL, provider="openai")
