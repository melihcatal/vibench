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
    if properties.dominant_colors:
        dominant_colors = [
            f"{color.color.red},{color.color.green},{color.color.blue}"
            for color in properties.dominant_colors.colors
        ]

    description = f"Image with dominant colors: {', '.join(dominant_colors)}. "

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations[:3]]
    description += f"Contains: {', '.join(labels)}."

    return ImageDescriptionResponse(
        provider="google_cloud_vision",
        model="image_properties",
        description=description.strip(),
    )
