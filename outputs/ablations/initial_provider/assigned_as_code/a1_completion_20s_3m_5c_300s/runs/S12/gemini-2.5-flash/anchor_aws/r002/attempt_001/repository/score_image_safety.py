import boto3
from typing import Dict, Any
from vision_client import get_rekognition_client
from vision_models import ImagePayload, DetectModerationLabelsResponse, ModerationLabel

def score_image_safety(payload: ImagePayload, config: Dict[str, Any]) -> DetectModerationLabelsResponse:
    client = get_rekognition_client(config)
    image_bytes = payload.image_bytes

    response = client.detect_moderation_labels(
        Image={'Bytes': image_bytes}
    )

    moderation_labels = []
    for label in response.get('ModerationLabels', []):
        moderation_labels.append(ModerationLabel(
            name=label['Name'],
            parent_name=label.get('ParentName'),
            confidence=label['Confidence'] / 100.0
        ))

    return DetectModerationLabelsResponse(moderation_labels=moderation_labels)
