import os
import boto3
from vision_client import get_rekognition_client
from vision_models import Label, LabelDetectionResponse

def detect_labels(image_path: str) -> LabelDetectionResponse:
    """
    Detects labels in an image using Amazon Rekognition.

    Args:
        image_path: The path to the local image file.

    Returns:
        A LabelDetectionResponse object containing the detected labels.
    """
    rekognition_client = get_rekognition_client()
    
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    response = rekognition_client.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=10,
        MinConfidence=75
    )

    labels = [
        Label(name=label['Name'], confidence=label['Confidence'])
        for label in response.get('Labels', [])
    ]
    
    return LabelDetectionResponse(labels=labels)
