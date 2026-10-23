import os
import boto3

def detect_image_labels(image_bytes: bytes) -> dict:
    """
    Detects labels (objects and scenes) in a static image using AWS Rekognition.

    Args:
        image_bytes: The image content in bytes.

    Returns:
        A dictionary containing the detected labels and their confidence scores.
    """
    rekognition_client = boto3.client(
        'rekognition',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    
    response = rekognition_client.detect_labels(
        Image={'Bytes': image_bytes}
    )
    
    labels = []
    for label in response.get('Labels', []):
        labels.append({
            'name': label.get('Name'),
            'confidence': label.get('Confidence')
        })
    return {'labels': labels}

