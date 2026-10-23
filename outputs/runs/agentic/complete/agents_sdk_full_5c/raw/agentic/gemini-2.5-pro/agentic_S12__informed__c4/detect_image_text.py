from google.cloud import vision
from vision_client import get_google_vision_client
from vision_models import TextAnnotation

def detect_text(image_path: str) -> list[TextAnnotation]:
    """
    Detects and extracts text from an image using Google Cloud Vision API OCR.

    Args:
        image_path: The path to the local image file.

    Returns:
        A list of TextAnnotation objects found in the image.
    """
    client = get_google_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )

    return [
        TextAnnotation(
            description=text.description,
            bounding_poly=[(v.x, v.y) for v in text.bounding_poly.vertices],
        )
        for text in texts
    ]
