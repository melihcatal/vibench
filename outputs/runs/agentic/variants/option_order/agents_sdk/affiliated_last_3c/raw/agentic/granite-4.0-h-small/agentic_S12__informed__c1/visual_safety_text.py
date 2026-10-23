import os
import boto3
import requests
from vision_models import normalize_labels

# AWS Rekognition client for content moderation
rekognition = boto3.client('rekognition',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1')


def flag_unsafe_labels(labels):
    """Use Amazon Comprehend toxic detection to flag unsafe visual labels."""
    # Simple placeholder: any label containing profanity is unsafe
    unsafe = [lbl for lbl in labels if any(bad in lbl.lower() for bad in ['kill','rape','bomb','terrorist'])]
    return unsafe
