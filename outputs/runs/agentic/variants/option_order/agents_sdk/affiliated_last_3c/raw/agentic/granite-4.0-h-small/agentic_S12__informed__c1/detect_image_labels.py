import os
import boto3
from vision_client import VisionClient

# Amazon Rekognition SDK client
rekognition = boto3.client('rekognition',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1')

def detect_image_labels(image_path):
    client = VisionClient(rekognition=rekognition)
    response = client.detect_labels(Image={'S3Object': {'Bucket': 'my-bucket', 'Name': image_path}})
    # Normalize response
    labels = [label['Name'] for label in response['Labels']]
    return labels
