from typing import List, Dict, Any
from vision_client import get_rekognition_client
from vision_models import ModerationLabel, ImageSafetyResponse

def score_image_safety(image_bytes: bytes) -> ImageSafetyResponse:
    """
    Checks an image for unsafe or policy-sensitive visual content using AWS Rekognition.

    Args:
        image_bytes: The image content as bytes.

    Returns:
        An ImageSafetyResponse object containing the detected moderation labels.
    """
    rekognition_client = get_rekognition_client()
    
    response = rekognition_client.detect_moderation_labels(
        Image={'Bytes': image_bytes}
    )

    moderation_labels = []
    for label_data in response.get('ModerationLabels', []):
        label = ModerationLabel(
            name=label_data.get('Name'),
            confidence=label_data.get('Confidence'),
            parent_name=label_data.get('ParentName')
        )
        moderation_labels.append(label)
    
    return ImageSafetyResponse(moderation_labels=moderation_labels)
