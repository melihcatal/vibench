import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from typing import Dict
from .vision_client import get_vision_client
from .vision_models import ImageDescriptionResponse


def describe_image(image_path: str) -> ImageDescriptionResponse:
    """Generates a short visual description for an image using Google Cloud Vision API."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.image_properties(image=image)
    properties = response.image_properties_annotation

    dominant_colors = []
    for color in properties.dominant_colors.colors:
        dominant_colors.append(
            {
                "red": color.color.red,
                "green": color.color.green,
                "blue": color.color.blue,
                "score": color.score,
                "pixel_fraction": color.pixel_fraction,
            }
        )

    description = f"Image with dominant colors: {[f'RGB({c["red"]}, {c["green"]}, {c["blue"]})' for c in dominant_colors]}"

    return ImageDescriptionResponse(
        provider="google_cloud_vision",
        model="image_properties",
        description=description,
        dominant_colors=dominant_colors,
    )
