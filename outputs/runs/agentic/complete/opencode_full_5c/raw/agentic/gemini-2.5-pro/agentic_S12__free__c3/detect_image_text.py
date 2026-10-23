from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageText


def detect_image_text(image_uri: str) -> list[ImageText]:
    """Detects text in an image using Google Cloud Vision."""
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    detected_texts = []
    for text in texts:
        vertices = [
            {"x": vertex.x, "y": vertex.y} for vertex in text.bounding_poly.vertices
        ]
        detected_texts.append(ImageText(text=text.description, bounding_poly=vertices))

    return detected_texts
