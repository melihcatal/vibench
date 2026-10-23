from __future__ import annotations

from typing import Optional

from openai import OpenAI

from vision_client import GOOGLE_VISION_PROVIDER, encode_image_base64, load_image_source
from vision_models import VisualDescription


OPENAI_MODEL = "gpt-4.1-mini"
OPENAI_PROVIDER = "openai"
SOURCE_PROVIDER = GOOGLE_VISION_PROVIDER


def describe_image(*, image_path: Optional[str] = None, image_uri: Optional[str] = None) -> VisualDescription:
    image = load_image_source(image_path=image_path, image_uri=image_uri)
    client = OpenAI()
    if image.image_bytes:
        image_input = {
            "type": "input_image",
            "image_url": f"data:{image.mime_type};base64,{encode_image_base64(image)}",
        }
    elif image.image_uri:
        image_input = {"type": "input_image", "image_url": image.image_uri}
    else:
        raise ValueError("Image input is required")

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Write a short, factual one-sentence description of this image."},
                    image_input,
                ],
            }
        ],
        max_output_tokens=80,
    )
    return VisualDescription(text=response.output_text.strip(), model=OPENAI_MODEL, provider=OPENAI_PROVIDER)
