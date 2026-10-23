from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import os
from typing import List, Dict
from .vision_client import get_vision_client
from .vision_models import ImageDescriptionResponse


def describe_image(image_path: str) -> ImageDescriptionResponse:
    """Generates a short visual description for an image using Google Cloud Vision."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.image_properties(image=image)
    properties = response.image_properties_annotation

    dominant_colors = [
        {
            "color": (prop.color.red, prop.color.green, prop.color.blue),
            "score": prop.score,
            "pixel_fraction": prop.pixel_fraction,
        }
        for prop in properties.dominant_colors.colors
    ]

    description = f"Image with dominant colors: {', '.join([f'RGB({c[0]}, {c[1]}, {c[2]})' for c in [dc['color'] for dc in dominant_colors]])}"

    return ImageDescriptionResponse(
        description=description, dominant_colors=dominant_colors
    )
