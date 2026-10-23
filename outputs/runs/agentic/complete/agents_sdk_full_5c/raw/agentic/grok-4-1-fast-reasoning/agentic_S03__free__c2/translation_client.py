"""
Provide local configuration and client helper utilities for General Text Translation
"""
import os
from typing import Dict, Any

def load_translation_config() -> Dict[str, str]:
    """Load all relevant environment variables for translation services."""
    return {
        "deepl_auth_key": os.getenv("DEEPL_AUTH_KEY"),
        "google_application_credentials": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        "azure_translator_key": os.getenv("AZURE_TRANSLATOR_KEY"),
        "azure_translator_region": os.getenv("AZURE_TRANSLATOR_REGION", "global"),
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "perspective_api_key": os.getenv("PERSPECTIVE_API_KEY"),
        "cohere_api_key": os.getenv("COHERE_API_KEY"),
    }
