import os
from google.cloud import vision
from typing import Dict, Any


def describe_image(image_path: str) -> Dict[str, Any]:
    """
    Generates a short visual description for an image using Google Cloud Vision API.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary containing image description and confidence score
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.image_properties(image=image)

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    description = "Image with "
    if response.image_properties_annotation.dominant_colors.colors:
        colors = response.image_properties_annotation.dominant_colors.colors
        color_descriptions = []
        for i, color in enumerate(colors[:3]):
            color_descriptions.append(
                f"RGB({color.color.red},{color.color.green},{color.color.blue})"
            )

        description += f"dominant colors: {', '.join(color_descriptions)}"

    label_response = client.label_detection(image=image)
    labels = label_response.label_annotations

    if labels:
        top_labels = [label.description for label in labels[:3]]
        description += f". Contains: {', '.join(top_labels)}"

    return {
        "description": description,
        "confidence": 0.95,
        "provider": "google-cloud-vision",
    }
