import os
import boto3
from google.cloud import vision
import google.generativeai as genai

def get_aws_rekognition_client():
    """
    Returns an initialized AWS Rekognition client.
    """
    return boto3.client(
        'rekognition',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

def get_google_vision_client():
    """
    Returns an initialized Google Cloud Vision client.
    """
    # Google Cloud Vision client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    return vision.ImageAnnotatorClient()

def configure_google_gemini():
    """
    Configures Google Gemini API with the API key.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def get_azure_content_moderator_config():
    """
    Returns Azure Content Moderator subscription key and endpoint.
    """
    subscription_key = os.environ.get("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")
    if not subscription_key or not endpoint:
        raise ValueError("Azure Content Moderator subscription key or endpoint not found in environment variables.")
    return subscription_key, endpoint
