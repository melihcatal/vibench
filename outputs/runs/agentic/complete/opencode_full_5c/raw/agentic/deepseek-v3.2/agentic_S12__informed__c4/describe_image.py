import os
from typing import Dict, Any
from vision_client import get_vision_client


def describe_image(image_path: str) -> Dict[str, Any]:
    """
    Generate a short visual description for an image using Amazon Rekognition.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary containing description text and confidence
    """
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.detect_labels(Image={"Bytes": image_bytes}, MaxLabels=20)

    labels = [label["Name"] for label in response["Labels"]]
    description = f"This image contains: {', '.join(labels[:5])}"

    return {
        "description": description,
        "labels": labels,
        "confidence": response["Labels"][0]["Confidence"]
        if response["Labels"]
        else 0.0,
    }
