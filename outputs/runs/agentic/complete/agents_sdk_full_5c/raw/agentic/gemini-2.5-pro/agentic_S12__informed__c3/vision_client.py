
import os
import boto3
from google.cloud import vision
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from clarifai.client.user import User

def get_google_vision_client() -> vision.ImageAnnotatorClient:
    """Initializes and returns a Google Cloud Vision client."""
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    return vision.ImageAnnotatorClient()

def get_azure_vision_client() -> ImageAnalysisClient:
    """Initializes and returns an Azure AI Vision client."""
    endpoint = os.environ["AZURE_VISION_ENDPOINT"]
    key = os.environ["AZURE_VISION_KEY"]
    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_rekognition_client():
    """Initializes and returns an Amazon Rekognition client."""
    return boto3.client(
        "rekognition",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

def get_clarifai_client() -> User:
    """Initializes and returns a Clarifai client."""
    # CLARIFAI_PAT should be set in the environment
    return User(user_id="me")
