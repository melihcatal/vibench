import io
from typing import Optional
from vision_client import get_vision_client
from vision_models import ImageDescription


def describe_image(image_path: str) -> Optional[ImageDescription]:
    """Generates a short visual description for an image using Google Cloud Vision API."""
    client = get_vision_client()

    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    image = {"content": content}
    response = client.image_properties(image=image)

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    dominant_colors = response.image_properties_annotation.dominant_colors.colors
    color_descriptions = [
        f"{color.score * 100:.0f}% {color.color.red},{color.color.green},{color.color.blue}"
        for color in dominant_colors[:3]
    ]

    description = f"Image with dominant colors: {', '.join(color_descriptions)}."
    return ImageDescription(description=description, confidence=0.85)
