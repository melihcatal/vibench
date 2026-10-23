from __future__ import annotations

from vision_client import openai_visual_response
from vision_models import ImageInput


def describe_image(image_path: str | None = None, image_url: str | None = None) -> str:
    image = ImageInput(image_path=image_path, image_url=image_url)
    result = openai_visual_response(
        "Provide a short, factual visual description of this image in one sentence.",
        image=image,
        model="gpt-4.1-mini",
    )
    return (result.get("output_text") or "").strip()
