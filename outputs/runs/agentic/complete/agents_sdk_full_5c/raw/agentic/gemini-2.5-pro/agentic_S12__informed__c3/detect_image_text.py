
import os
import boto3
from vision_client import get_rekognition_client
from vision_models import DetectedText

def detect_text(image_path: str) -> list[DetectedText]:
    """
    Detects text in an image using Amazon Rekognition.
    """
    client = get_rekognition_client()

    with open(image_path, 'rb') as image_file:
        source_bytes = image_file.read()

    response = client.detect_text(Image={'Bytes': source_bytes})
    
    text_detections = response.get('TextDetections', [])

    return [
        DetectedText(
            text=item['DetectedText'],
            confidence=item['Confidence'],
            box_id=item['Id']
        )
        for item in text_detections
        if item['Type'] == 'LINE'
    ]
