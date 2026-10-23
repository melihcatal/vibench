import boto3
import os

def get_kms_client():
    """
    Provides a configured AWS KMS client.
    Assumes AWS credentials and region are configured via environment variables
    or AWS CLI configuration.
    """
    region = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('kms', region_name=region)

def get_azure_content_safety_config():
    """
    Provides configuration for Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")
    return {"endpoint": endpoint, "key": key}

def get_gemini_api_key():
    """
    Provides the Google Gemini API key.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")
    return api_key

def get_google_cloud_translation_client():
    """
    Provides a Google Cloud Translation client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS or similar authentication is set up.
    """
    from google.cloud import translate_v3
    return translate_v3.TranslationServiceClient()
