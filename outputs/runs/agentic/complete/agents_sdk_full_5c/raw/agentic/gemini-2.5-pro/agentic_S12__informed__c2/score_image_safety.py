from vision_client import get_rekognition_client
from vision_models import SafetyLabel, SafetyResponse

def score_image_safety(image_path: str) -> SafetyResponse:
    """
    Detects moderation labels in an image using Amazon Rekognition.

    Args:
        image_path: The path to the local image file.

    Returns:
        A SafetyResponse object containing any detected moderation labels.
    """
    rekognition_client = get_rekognition_client()

    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    response = rekognition_client.detect_moderation_labels(
        Image={'Bytes': image_bytes}
    )

    safety_labels = [
        SafetyLabel(
            name=label['Name'],
            confidence=label['Confidence'],
            parent_name=label.get('ParentName', '')
        )
        for label in response.get('ModerationLabels', [])
    ]

    return SafetyResponse(safety_labels=safety_labels)
