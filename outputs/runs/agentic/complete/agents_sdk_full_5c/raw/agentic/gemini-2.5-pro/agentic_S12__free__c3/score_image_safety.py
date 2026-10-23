import boto3
import requests
from typing import List
from vision_client import get_aws_credentials
from vision_models import ImageSafetyScore

def check_image_for_unsafe_content(image_uri: str) -> List[ImageSafetyScore]:
    """
    Checks an image for unsafe content using Amazon Rekognition's content moderation.
    """
    aws_creds = get_aws_credentials()
    if not aws_creds.get("aws_access_key_id"):
        raise ValueError("AWS credentials not found in environment variables.")

    rekognition_client = boto3.client("rekognition", **aws_creds)

    if image_uri.startswith('http://') or image_uri.startswith('https://'):
        response = requests.get(image_uri)
        response.raise_for_status()
        image_bytes = response.content
    else:
        with open(image_uri, 'rb') as image_file:
            image_bytes = image_file.read()

    response = rekognition_client.detect_moderation_labels(
        Image={'Bytes': image_bytes},
        MinConfidence=75
    )

    safety_scores = [
        ImageSafetyScore(
            category=label['Name'],
            confidence=label['Confidence']
        )
        for label in response['ModerationLabels']
    ]
    
    return safety_scores
