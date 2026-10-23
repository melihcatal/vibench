from google.cloud import vision
from vision_client import get_google_vision_client
from vision_models import DetectedText


def detect_text(image_uri: str) -> list[DetectedText]:
    """Detects text entities in the image located at the given URI."""
    client = get_google_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(f"Google Vision API error: {response.error.message}")

    # The first annotation is the full text block.
    if response.text_annotations:
        full_text_annotation = response.text_annotations[0]
        return [
            DetectedText(
                text=full_text_annotation.description,
                confidence=1.0,  # Confidence is not provided per block in this API
            )
        ]
    return []
