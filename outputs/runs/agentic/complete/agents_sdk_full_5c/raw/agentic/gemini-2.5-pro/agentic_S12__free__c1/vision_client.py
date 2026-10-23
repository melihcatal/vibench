import os

import boto3
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import aiplatform
import openai


def get_aws_rekognition_client():
    """Initializes and returns a Boto3 Rekognition client."""
    return boto3.client(
        "rekognition",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

def get_google_vertex_ai_client():
    """Initializes the Google Vertex AI client."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    aiplatform.init(project=project_id, location=location)
    return aiplatform

def get_azure_vision_client():
    """Initializes and returns an Azure AI Vision client."""
    return ImageAnalysisClient(
        endpoint=os.environ.get("AZURE_VISION_ENDPOINT"),
        credential=AzureKeyCredential(os.environ.get("AZURE_VISION_KEY"))
    )

def get_openai_client():
    """Initializes and returns the OpenAI client."""
    api_key = os.environ.get("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)

def get_s3_compatible_client(endpoint_url, access_key_id, secret_access_key, region_name="auto"):
    """Initializes a Boto3 client for an S3-compatible service like Cloudflare R2."""
    return boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name=region_name
    )
