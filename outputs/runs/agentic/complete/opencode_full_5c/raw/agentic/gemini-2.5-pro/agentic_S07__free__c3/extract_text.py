from google.cloud import vision
from document_client import get_google_vision_client


def extract_text_from_image(image_path: str) -> str:
    """
    Extracts plain text from a local image file using Google Cloud Vision API.
    """
    client = get_google_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    return ""
