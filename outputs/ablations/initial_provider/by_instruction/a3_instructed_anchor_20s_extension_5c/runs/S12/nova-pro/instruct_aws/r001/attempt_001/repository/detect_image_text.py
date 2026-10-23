import boto3
from vision_client import VisionClient

def detect_image_text(image_path):
    client = VisionClient()
    response = client.detect_text(image_path)
    return response['TextDetections']