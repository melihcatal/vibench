import os
from google.cloud import vision
from typing import List, Dict, Any


def detect_image_text(image_path: str) -> List[Dict[str, Any]]:
    """
    Detects text appearing inside an image using Google Cloud Vision API.

    Args:
        image_path: Path to the image file

    Returns:
        List of dictionaries containing detected text and bounding boxes
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    results = []
    if texts:
        full_text = texts[0].description
        results.append({"text": full_text, "type": "full_text", "confidence": 0.95})

        for i, text in enumerate(texts[1:11] if len(texts) > 11 else texts[1:]):
            vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
            results.append(
                {
                    "text": text.description,
                    "bounding_box": vertices,
                    "confidence": text.confidence
                    if hasattr(text, "confidence")
                    else 0.8,
                    "type": "text_block",
                }
            )

    return results
