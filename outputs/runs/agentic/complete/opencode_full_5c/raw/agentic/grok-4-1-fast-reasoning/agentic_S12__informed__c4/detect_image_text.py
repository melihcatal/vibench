from google.cloud import vision
from vision_client import load_image_bytes


def detect_image_text(image_path: str) -> dict:
    """
    Detects text appearing inside an image using Google Cloud Vision.
    Returns: {'texts': [str, ...]}
    Requires GOOGLE_APPLICATION_CREDENTIALS
    """
    image_bytes = load_image_bytes(image_path)

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)

    response = client.text_detection(image=image)

    texts = []
    if response.text_annotations:
        texts = [ta.description.strip() for ta in response.text_annotations[1:]]

    return {"texts": texts}
