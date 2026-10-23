from vision_client import get_google_vision_client
from vision_models import ImageText, ImageTexts
from google.cloud import vision


def detect_image_text(image_uri: str) -> ImageTexts:
    client = get_google_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    detected_texts = []
    if texts:
        # The first element is the full text block, subsequent elements are individual words.
        # We'll just take the full block.
        full_text_annotation = texts[0]
        bounding_box = [
            {"x": vertex.x, "y": vertex.y}
            for vertex in full_text_annotation.bounding_poly.vertices
        ]
        detected_texts.append(
            ImageText(
                text=full_text_annotation.description,
                confidence=full_text_annotation.score,
                bounding_box=bounding_box,
            )
        )

    return ImageTexts(texts=detected_texts)
