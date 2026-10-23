import boto3
from vision_client import VisionClient

def detect_image_labels(image_path):
    client = VisionClient()
    response = client.detect_labels(image_path)
    return response['Labels']