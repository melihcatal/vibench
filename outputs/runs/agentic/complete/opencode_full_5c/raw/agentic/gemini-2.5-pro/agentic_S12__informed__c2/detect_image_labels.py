from vision_client import get_vision_client
from vision_models import LabelAnnotation
from google.cloud import vision
from typing import List


def detect_image_labels(image_uri: str) -> List[LabelAnnotation]:
    """
    Detects labels in an image using the Google Cloud Vision API.

    Args:
        image_uri: The URI of the image (e.g., a GCS path like "gs://...").

    Returns:
        A list of LabelAnnotation objects.
    """
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.label_detection(image=image)

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )

    labels = [
        LabelAnnotation(
            mid=label.mid,
            description=label.description,
            score=label.score,
            topicality=label.topicality,
        )
        for label in response.label_annotations
    ]
    return labels
