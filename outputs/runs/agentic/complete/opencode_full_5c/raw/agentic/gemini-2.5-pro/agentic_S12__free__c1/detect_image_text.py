from google.cloud import vision
from vision_client import get_vision_client
from vision_models import TextAnnotation


def detect_text(image_path: str) -> list[TextAnnotation]:
    client = get_vision_client()
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    return [
        TextAnnotation(
            description=text.description,
            bounding_poly=[
                {"x": vertex.x, "y": vertex.y} for vertex in text.bounding_poly.vertices
            ],
        )
        for text in texts
    ]
