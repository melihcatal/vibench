import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class VisionClientConfig:
    google_credentials_path: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_key: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: Optional[str] = None
    azure_content_safety_endpoint: Optional[str] = None
    azure_content_safety_key: Optional[str] = None

def load_vision_client_config() -> VisionClientConfig:
    return VisionClientConfig(
        google_credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_openai_key=os.getenv("AZURE_OPENAI_API_KEY"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
        azure_content_safety_endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
        azure_content_safety_key=os.getenv("AZURE_CONTENT_SAFETY_KEY")
    )

def initialize_google_vision_client():
    from google.cloud import vision
    return vision.ImageAnnotatorClient()

def initialize_aws_rekognition_client():
    import boto3
    return boto3.client(
        "rekognition",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )