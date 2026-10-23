from __future__ import annotations

from typing import Optional

from vision_client import OPENAI_VISION_MODEL, build_openai_image_input, get_openai_client
from vision_models import ImageDescriptionResult, ImageSource


def describe_image(image_path: Optional[str] = None, image_url: Optional[str] = None) -> ImageDescriptionResult:
    client = get_openai_client()
    source = ImageSource(image_path=image_path, image_url=image_url)
    response = client.responses.create(
        model=OPENAI_VISION_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Provide a short visual description of this image in one sentence."},
                    build_openai_image_input(source),
                ],
            }
        ],
        max_output_tokens=80,
    )
    description = getattr(response, "output_text", "").strip()
    return ImageDescriptionResult(description=description, model=OPENAI_VISION_MODEL, raw_response=response.model_dump())
