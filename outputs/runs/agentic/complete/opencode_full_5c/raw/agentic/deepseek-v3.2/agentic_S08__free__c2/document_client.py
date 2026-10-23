import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ClientConfig:
    azure_endpoint: Optional[str] = None
    azure_key: Optional[str] = None
    google_credentials_path: Optional[str] = None
    openai_api_key: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_translate_key: Optional[str] = None
    mongodb_uri: Optional[str] = None


def load_config() -> ClientConfig:
    """
    Load configuration from environment variables.
    """
    return ClientConfig(
        azure_endpoint=os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT"),
        azure_key=os.getenv("AZURE_FORM_RECOGNIZER_KEY"),
        google_credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        google_translate_key=os.getenv("GOOGLE_TRANSLATE_API_KEY"),
        mongodb_uri=os.getenv("MONGODB_URI"),
    )


def get_azure_form_recognizer_client():
    """
    Get Azure Form Recognizer client.
    """
    config = load_config()
    if not config.azure_endpoint or not config.azure_key:
        raise ValueError("Azure Form Recognizer credentials not configured")

    from azure.ai.formrecognizer import DocumentAnalysisClient
    from azure.core.credentials import AzureKeyCredential

    client = DocumentAnalysisClient(
        endpoint=config.azure_endpoint, credential=AzureKeyCredential(config.azure_key)
    )
    return client


def get_google_vision_client():
    """
    Get Google Cloud Vision client.
    """
    config = load_config()
    if not config.google_credentials_path:
        raise ValueError("Google Cloud credentials not configured")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.google_credentials_path

    from google.cloud import vision

    client = vision.ImageAnnotatorClient()
    return client


def get_openai_client():
    """
    Get OpenAI client.
    """
    config = load_config()
    if not config.openai_api_key:
        raise ValueError("OpenAI API key not configured")

    import openai

    openai.api_key = config.openai_api_key
    return openai


def get_aws_comprehend_client():
    """
    Get AWS Comprehend client.
    """
    config = load_config()
    if not config.aws_access_key_id or not config.aws_secret_access_key:
        raise ValueError("AWS credentials not configured")

    import boto3

    client = boto3.client(
        "comprehend",
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        region_name=config.aws_region,
    )
    return client


def get_anthropic_client():
    """
    Get Anthropic Claude client.
    """
    config = load_config()
    if not config.anthropic_api_key:
        raise ValueError("Anthropic API key not configured")

    import anthropic

    client = anthropic.Anthropic(api_key=config.anthropic_api_key)
    return client


def get_google_translate_client():
    """
    Get Google Translate client.
    """
    config = load_config()
    if not config.google_translate_key:
        raise ValueError("Google Translate API key not configured")

    from google.cloud import translate_v2 as translate

    client = translate.Client(credentials=config.google_translate_key)
    return client


def get_mongodb_client():
    """
    Get MongoDB client.
    """
    config = load_config()
    if not config.mongodb_uri:
        raise ValueError("MongoDB URI not configured")

    from pymongo import MongoClient

    client = MongoClient(config.mongodb_uri)
    return client
