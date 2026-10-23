"""
[SAME-SCENARIO] detect_image_labels.py - detects labels or objects in a static image
"""

import vision_client
from vision_models import Label, VisionResult
from typing import List

def detect_labels(image_path: str) -> VisionResult:
    """
    Detects labels in an image using AWS Rekognition.
    """
    rekognition = vision_client.get_vision_client()
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    response = rekognition.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=20,
        MinConfidence=80.0
    )

    labels = [
        Label(name=label['Name'], confidence=label['Confidence'])
        for label in response.get('Labels', [])
    ]
    
    return VisionResult(labels=labels)

