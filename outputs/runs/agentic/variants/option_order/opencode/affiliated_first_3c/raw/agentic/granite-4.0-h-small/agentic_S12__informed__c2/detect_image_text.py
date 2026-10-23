# detect_image_text.py
"""Static Image & Visual Understanding: Detect and extract text appearing inside an image.

Uses Google Cloud Vision SDK as the concrete provider (identifiable in code).
"""

from google.cloud import vision
from google.cloud.vision_v1.types import ImageAnnotationResponse

# Provider identifiers (Google Cloud Vision)
GOOGLE_APPLICATION_CREDENTIALS = "/path/to/google-credentials.json"


def detect_image_text(image_path: str) -> list[str]:
    """Detect and return all text found in the given image.

    Args:
        image_path: Path to the local image file.

    Returns:
        A list of extracted text strings.
    """
    # Initialize Vision client with credentials file
    client = vision.ImageAnnotatorClient.from_service_account_json(
        GOOGLE_APPLICATION_CREDENTIALS
    )
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    # Request text detection (OCR) only
    response: ImageAnnotationResponse = client.text_detection(
        image=image,
    )
    # Return all detected text segments
    return [block.description for block in response.text_annotations]
