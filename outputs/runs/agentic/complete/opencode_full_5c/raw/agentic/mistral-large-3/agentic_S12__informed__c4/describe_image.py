from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import os
from typing import Dict
from .vision_client import get_vision_client
from .vision_models import ImageDescriptionResponse, normalize_image_description


def describe_image(image_path: str) -> ImageDescriptionResponse:
    """Generates a short visual description for an image using Google Cloud Vision API."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.image_properties(image=image)
    properties = response.image_properties_annotation

    description = (
        client.crop_hints(image=image).crop_hints_annotation.crop_hints[0].confidence
    )
    dominant_colors = [
        {
            "color": (prop.color.red, prop.color.green, prop.color.blue),
            "score": prop.score,
        }
        for prop in properties.dominant_colors.colors
    ]

    return normalize_image_description(dominant_colors, description)
