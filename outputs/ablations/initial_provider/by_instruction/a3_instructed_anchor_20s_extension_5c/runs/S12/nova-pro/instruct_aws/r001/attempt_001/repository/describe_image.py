import boto3
from vision_client import VisionClient

def describe_image(image_path):
    client = VisionClient()
    response = client.describe_image(image_path)
    return response['Description']