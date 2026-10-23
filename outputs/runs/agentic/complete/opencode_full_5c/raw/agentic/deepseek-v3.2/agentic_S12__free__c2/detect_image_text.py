import os
from google.cloud import vision
from vision_client import get_vision_client


def detect_image_text(image_path):
    """Detects text appearing inside an image using Google Cloud Vision API."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        full_text = texts[0].description
        detected_texts = []

        for text in texts[1:]:
            detected_texts.append(
                {
                    "text": text.description,
                    "bounding_poly": [
                        (vertex.x, vertex.y) for vertex in text.bounding_poly.vertices
                    ],
                }
            )

        return {"full_text": full_text, "text_blocks": detected_texts}

    return {"full_text": "", "text_blocks": []}
