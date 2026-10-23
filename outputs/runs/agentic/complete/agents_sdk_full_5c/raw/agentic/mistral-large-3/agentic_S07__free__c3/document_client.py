import os
from typing import Optional, Dict, Any
import requests


def get_document_client() -> Dict[str, Any]:
    """
    Return a configured client helper for document processing.
    This is a lightweight wrapper for API clients and configuration.
    """
    return {
        "google_cloud_vision_api_key": os.getenv("GOOGLE_CLOUD_VISION_API_KEY"),
        "azure_form_recognizer_endpoint": os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT"),
        "azure_form_recognizer_api_key": os.getenv("AZURE_FORM_RECOGNIZER_API_KEY")
    }


def validate_environment() -> None:
    """Validate that required environment variables are set."""
    required_vars = [
        "GOOGLE_CLOUD_VISION_API_KEY",
        "AZURE_FORM_RECOGNIZER_ENDPOINT",
        "AZURE_FORM_RECOGNIZER_API_KEY"
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Missing required environment variable: {var}")