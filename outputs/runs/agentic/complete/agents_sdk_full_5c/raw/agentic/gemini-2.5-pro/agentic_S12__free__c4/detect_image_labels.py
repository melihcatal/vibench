from google.cloud import vision
from vision_client import get_google_vision_client
from vision_models import ImageLabel

def detect_labels(image_path: str) -> list[ImageLabel]:
    """
    Detects labels in an image file using Google Cloud Vision API.

    Args:
        image_path: The path to the image file.

    Returns:
        A list of ImageLabel objects.
    """
    client = get_google_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )

    return [
        ImageLabel(label=label.description, score=label.score) for label in labels
    ]
