from vision_client import get_aws_rekognition_client
from vision_models import ImageSafetyScore

def score_image_safety(image_path: str) -> list[ImageSafetyScore]:
    """
    Checks an image for unsafe content using Amazon Rekognition.

    Args:
        image_path: The path to the image file.

    Returns:
        A list of ImageSafetyScore objects for any detected moderation labels.
    """
    rekognition_client = get_aws_rekognition_client()

    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    response = rekognition_client.detect_moderation_labels(
        Image={'Bytes': image_bytes}
    )

    safety_scores = []
    for label in response['ModerationLabels']:
        safety_scores.append(
            ImageSafetyScore(
                category=label['Name'],
                confidence=label['Confidence'] / 100.0,
            )
        )
    return safety_scores
