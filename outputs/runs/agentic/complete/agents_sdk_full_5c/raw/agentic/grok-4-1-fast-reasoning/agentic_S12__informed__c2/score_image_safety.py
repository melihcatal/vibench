import boto3
from .vision_client import image_to_bytes
from .vision_models import ModerationLabel, VisionSafety

def score_image_safety(image_path: str) -> VisionSafety:
    rekognition = boto3.client('rekognition')
    image_bytes = image_to_bytes(image_path)
    response = rekognition.detect_moderation_labels(
        Image={'Bytes': image_bytes},
        MinConfidence=60
    )
    moderation_labels = []
    for label_group in response.get('ModerationLabels', []):
        parent_name = label_group.get('ParentName')
        for chip in label_group.get('ModerationLabelChips', []):
            moderation_labels.append({
                'name': chip['Name'],
                'confidence': chip['Confidence'],
                'parent_name': parent_name
            })
    is_unsafe = any(label['confidence'] > 80 for label in moderation_labels)
    return {
        'moderation_labels': moderation_labels,
        'is_unsafe': is_unsafe
    }