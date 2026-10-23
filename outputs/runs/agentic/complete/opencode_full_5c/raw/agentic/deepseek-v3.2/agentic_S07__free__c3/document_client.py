import os
from typing import Optional
import boto3
from google.cloud import vision
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


def get_google_vision_client() -> vision.ImageAnnotatorClient:
    """
    Get Google Cloud Vision client with credentials from environment.
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    return vision.ImageAnnotatorClient()


def get_amazon_textract_client():
    """
    Get Amazon Textract client with credentials from environment.
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS credentials not configured")

    return boto3.client(
        "textract",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )


def get_azure_form_recognizer_client():
    """
    Get Azure Form Recognizer endpoint and key from environment.
    Returns tuple of (endpoint, api_key).
    """
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    api_key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

    return endpoint, api_key


def get_google_document_ai_client() -> documentai.DocumentProcessorServiceClient:
    """
    Get Google Document AI client with credentials from environment.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    return documentai.DocumentProcessorServiceClient(client_options=client_options)


def get_openai_client():
    """
    Get OpenAI client for translation and embedding tasks.
    """
    import openai

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    openai.api_key = api_key
    return openai


def get_google_translate_client():
    """
    Get Google Cloud Translation client.
    """
    from google.cloud import translate_v2 as translate

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    return translate.Client()


def get_perspective_api_client():
    """
    Get Perspective API client for content safety checks.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    return api_key
