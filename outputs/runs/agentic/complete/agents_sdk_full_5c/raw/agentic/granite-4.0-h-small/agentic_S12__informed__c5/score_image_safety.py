import os
from vision_client import VisionClient
from vision_models import normalize_safety

def score_image_safety(image_path):
    """Checks an image for unsafe visual content using AWS Rekognition.
    Returns a boolean indicating whether the image is SAFE.
    """
    client = VisionClient(service='rekognition')
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    response = client.detect_moderation_labels(Image={'Bytes': image_bytes})
    # ModerationLabels returns [{"Confidence": ..., "Name": ...}, ...]
    unsafe_labels = [
        label['Name'] 
        for label in response.get('ModerationLabels', [])
        if label['Confidence'] > 50.0  # treat >50% as concerning
    ]
    is_safe = len(unsafe_labels) == 0
    return is_safe
