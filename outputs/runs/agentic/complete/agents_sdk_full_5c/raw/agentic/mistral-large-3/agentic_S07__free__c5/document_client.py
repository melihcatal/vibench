import os
from typing import Optional, Dict, Any
import requests


def get_document_client() -> Any:
    """
    Return a configured client for document processing.
    Currently supports Google Cloud Vision, Azure Form Recognizer, and Amazon Textract.
    """
    provider = os.getenv("DOCUMENT_PROVIDER", "google_cloud_vision")
    
    if provider == "google_cloud_vision":
        return GoogleCloudVisionClient()
    elif provider == "azure_form_recognizer":
        return AzureFormRecognizerClient()
    elif provider == "amazon_textract":
        return AmazonTextractClient()
    else:
        raise ValueError(f"Unsupported provider: {provider}")


class GoogleCloudVisionClient:
    """Client for Google Cloud Vision API."""
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_CLOUD_VISION_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_CLOUD_VISION_API_KEY environment variable not set")


class AzureFormRecognizerClient:
    """Client for Azure Form Recognizer."""
    def __init__(self):
        self.endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        self.key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
        if not self.endpoint or not self.key:
            raise ValueError("AZURE_FORM_RECOGNIZER_ENDPOINT or AZURE_FORM_RECOGNIZER_KEY not set")


class AmazonTextractClient:
    """Client for Amazon Textract."""
    def __init__(self):
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise ValueError("AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY not set")