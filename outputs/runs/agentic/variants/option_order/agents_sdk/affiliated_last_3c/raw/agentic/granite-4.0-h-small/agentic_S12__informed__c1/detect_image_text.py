import os
import boto3
from vision_client import VisionClient

# Amazon Rekognition SDK client
rekognition = boto3.client('rekognition',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1')

def detect_image_text(image_path):
    client = VisionClient(rekognition=rekognition)
    response = client.detect_text(Image={'S3Object': {'Bucket': 'my-bucket', 'Name': image_path}})
    texts = [text['DetectedText'] for text in response.get('TextDetections', [])]
    return texts
