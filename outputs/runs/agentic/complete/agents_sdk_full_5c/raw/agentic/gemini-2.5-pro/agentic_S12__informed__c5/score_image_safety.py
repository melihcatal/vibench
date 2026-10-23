"""
[SAME-SCENARIO] score_image_safety.py - checks an image for unsafe or policy-sensitive visual content
"""

import vision_client
from vision_models import ModerationLabel, VisionResult
from typing import List

def check_safety(image_path: str) -> VisionResult:
    """
    Checks an image for unsafe content using AWS Rekognition.
    """
    rekognition = vision_client.get_vision_client()
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    response = rekognition.detect_moderation_labels(
        Image={'Bytes': image_bytes},
        MinConfidence=75.0
    )

    moderation_labels = [
        ModerationLabel(name=label['Name'], confidence=label['Confidence'])
        for label in response.get('ModerationLabels', [])
    ]
    
    return VisionResult(moderation_labels=moderation_labels)

