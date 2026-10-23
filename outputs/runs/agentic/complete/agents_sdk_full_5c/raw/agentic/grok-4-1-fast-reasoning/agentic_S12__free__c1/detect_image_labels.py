import boto3
from vision_client import load_image_bytes
from vision_models import ImageLabels

def detect_image_labels(image_path: str) -> ImageLabels:
    rekognition = boto3.client('rekognition', region_name='us-east-1')
    image_bytes = load_image_bytes(image_path)
    response = rekognition.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=10,
        MinConfidence=80.0
    )
    labels = [label['Name'] for label in response['Labels']]
    confidences = [label['Confidence'] for label in response['Labels']]
    return ImageLabels(labels=labels, confidences=confidences)