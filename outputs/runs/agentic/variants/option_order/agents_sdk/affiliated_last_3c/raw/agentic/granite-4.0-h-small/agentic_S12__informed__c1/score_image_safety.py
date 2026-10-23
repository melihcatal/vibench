import os
import boto3
from vision_client import VisionClient

# Amazon Rekognition SDK client
rekognition = boto3.client('rekognition',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1')

def score_image_safety(image_path):
    client = VisionClient(rekognition=rekognition)
    response = client.detect_moderation_labels(Image={'S3Object': {'Bucket': 'my-bucket', 'Name': image_path}})
    # Simplify unsafe content detection
    unsafe = any(label['Name'] in ['Explicit Nudity', 'Suggestive'] for label in response.get('ModerationLabels', []))
    return unsafe
