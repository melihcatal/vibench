from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageText


def detect_text(image_path: str) -> list[ImageText]:
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    detected_texts = []
    if texts:
        # The first element is the full text, subsequent are individual words/symbols.
        # We can just return the full text block.
        full_text = texts[0]
        vertices = [(vertex.x, vertex.y) for vertex in full_text.bounding_poly.vertices]
        detected_texts.append(
            ImageText(description=full_text.description, bounding_poly=vertices)
        )

    return detected_texts
