import os
from typing import List, Dict, Any
from google.cloud import vision


def detect_image_text(image_path: str) -> List[Dict[str, Any]]:
    """
    Detect text appearing inside an image using Google Cloud Vision.

    Args:
        image_path: Path to the image file

    Returns:
        List of dictionaries containing detected text information
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    if not texts:
        return []

    result = []
    for text in texts[1:]:  # Skip the first element which contains all text
        vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        result.append(
            {
                "text": text.description,
                "confidence": text.confidence if hasattr(text, "confidence") else None,
                "bounding_box": vertices,
            }
        )

    return result
