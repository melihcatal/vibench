"""
[SAME-SCENARIO] detect_image_text.py - detects text appearing inside an image
"""

import vision_client
from vision_models import TextDetection, VisionResult
from typing import List

def detect_text(image_path: str) -> VisionResult:
    """
    Detects text in an image using AWS Rekognition.
    """
    rekognition = vision_client.get_vision_client()
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    response = rekognition.detect_text(Image={'Bytes': image_bytes})

    text_detections = [
        TextDetection(
            text=detection['DetectedText'],
            confidence=detection['Confidence'],
            box=[
                detection['Geometry']['BoundingBox']['Left'],
                detection['Geometry']['BoundingBox']['Top'],
                detection['Geometry']['BoundingBox']['Width'],
                detection['Geometry']['BoundingBox']['Height'],
            ]
        )
        for detection in response.get('TextDetections', []) if detection['Type'] == 'LINE'
    ]

    return VisionResult(text_detections=text_detections)
