import boto3
from vision_client import VisionClient

def score_image_safety(image_path):
    client = VisionClient()
    response = client.check_safety(image_path)
    return response['ModerationLabels']