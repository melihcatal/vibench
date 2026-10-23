import os
import boto3
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

def get_rekognition_client():
    """Initializes and returns a Boto3 client for Amazon Rekognition."""
    return boto3.client(
        'rekognition',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

def get_azure_vision_client():
    """Initializes and returns a client for Azure AI Vision."""
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    key = os.getenv("AZURE_VISION_KEY")
    if not endpoint or not key:
        raise ValueError("Azure Vision endpoint and key must be set in environment variables.")
    
    return ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )
