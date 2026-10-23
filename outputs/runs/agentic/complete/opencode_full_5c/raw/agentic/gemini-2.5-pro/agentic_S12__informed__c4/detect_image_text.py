from google.cloud import vision
from vision_client import get_google_vision_client
from vision_models import ImageText, BoundingBox


def detect_image_text(image_bytes: bytes) -> list[ImageText]:
    client = get_google_vision_client()
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    detected_texts = []
    for text in texts[1:]:  # Skip the first one which is the full text
        vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        bounding_box = BoundingBox(
            x_min=min(v[0] for v in vertices),
            y_min=min(v[1] for v in vertices),
            x_max=max(v[0] for v in vertices),
            y_max=max(v[1] for v in vertices),
        )
        detected_texts.append(
            ImageText(text=text.description, bounding_box=bounding_box)
        )

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return detected_texts
