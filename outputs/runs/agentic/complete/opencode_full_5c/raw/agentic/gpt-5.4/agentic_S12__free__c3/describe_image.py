from __future__ import annotations

from vision_client import openai_vision_response
from vision_models import ImageDescriptionResult, ImageSource


def describe_image(image: ImageSource) -> ImageDescriptionResult:
    response = openai_vision_response(
        image,
        "Describe this image in one short sentence suitable for alt text.",
    )
    description = response["output"][0]["content"][0]["text"].strip()
    return ImageDescriptionResult(
        provider="openai", description=description, raw_response=response
    )
