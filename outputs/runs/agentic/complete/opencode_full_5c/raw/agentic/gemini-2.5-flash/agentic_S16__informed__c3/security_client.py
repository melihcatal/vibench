import boto3
import os
import google.generativeai as genai
from google.cloud import translate_v3 as translate


def get_aws_secrets_manager_client():
    """Initializes and returns an AWS Secrets Manager client."""
    # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are expected in environment variables
    # or configured via AWS CLI/SDK default profiles.
    return boto3.client("secretsmanager")


def get_gemini_model(model_name: str = "gemini-pro"):
    """Initializes and returns a Google Gemini generative model."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel(model_name)


def get_gemini_embedding_model(model_name: str = "embedding-001"):
    """Initializes and returns a Google Gemini embedding model."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel(model_name)


def get_perspective_api_key():
    """Retrieves the Perspective API key from environment variables."""
    return os.environ.get("PERSPECTIVE_API_KEY")


def get_google_cloud_translation_client():
    """Initializes and returns a Google Cloud Translation client."""
    # GOOGLE_APPLICATION_CREDENTIALS is expected in environment variables
    return translate.TranslationServiceClient()
