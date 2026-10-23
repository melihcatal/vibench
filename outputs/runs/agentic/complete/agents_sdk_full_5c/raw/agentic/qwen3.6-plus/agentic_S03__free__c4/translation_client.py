"""
Local configuration and client helper utilities for General Text Translation.
Provides provider-specific client initialization and configuration management
for Google Cloud Translation API.
"""

import os
from typing import Optional, Dict, Any

from google.cloud import translate_v2 as translate
from google.api_core import client_info


# Google Cloud Translation provider identifiers
GOOGLE_TRANSLATE_API_ENDPOINT = "translate.googleapis.com"
GOOGLE_TRANSLATE_V2_MODEL = "google-translate-v2"
GOOGLE_CLOUD_TRANSLATION_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
GOOGLE_APPLICATION_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"


def get_google_translate_config() -> Dict[str, Any]:
    """Load Google Cloud Translation configuration from environment."""
    config = {
        "project_id": os.environ.get(GOOGLE_CLOUD_TRANSLATION_PROJECT_ENV, ""),
        "credentials_path": os.environ.get(GOOGLE_APPLICATION_CREDENTIALS_ENV),
        "api_endpoint": GOOGLE_TRANSLATE_API_ENDPOINT,
        "model": GOOGLE_TRANSLATE_V2_MODEL,
        "timeout_seconds": int(os.environ.get("GOOGLE_TRANSLATE_TIMEOUT", "30")),
    }
    return config


def create_translate_client(
    project_id: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> translate.Client:
    """
    Create and configure a Google Cloud Translation v2 client.
    
    Args:
        project_id: Google Cloud project ID. Falls back to env var.
        credentials_path: Path to service account JSON credentials.
    
    Returns:
        Configured google.cloud.translate_v2.Client instance.
    """
    config = get_google_translate_config()
    
    if project_id:
        config["project_id"] = project_id
    
    if credentials_path:
        os.environ[GOOGLE_APPLICATION_CREDENTIALS_ENV] = credentials_path
    
    client_info_data = client_info.ClientInfo(
        user_agent="general-text-translation-service/1.0"
    )
    
    client = translate.Client(
        project=config["project_id"],
        client_info=client_info_data,
    )
    
    return client


def get_supported_languages(
    client: translate.Client,
    target_language: str = "en",
) -> list:
    """
    Retrieve list of supported languages from Google Translate API.
    
    Args:
        client: Google Cloud Translation client.
        target_language: Language code for language names.
    
    Returns:
        List of dicts with 'language' and 'name' keys.
    """
    languages = client.get_languages(target_language=target_language)
    return languages


def detect_language(
    client: translate.Client,
    text: str,
) -> Dict[str, Any]:
    """
    Detect the language of input text using Google Translate API.
    
    Args:
        client: Google Cloud Translation client.
        text: Text to detect language for.
    
    Returns:
        Dict with 'language', 'confidence', and 'is_reliable' keys.
    """
    detections = client.detect_language(text)
    
    if isinstance(detections, list) and len(detections) > 0:
        return {
            "language": detections[0].get("language", "unknown"),
            "confidence": detections[0].get("confidence", 0.0),
            "is_reliable": detections[0].get("isReliable", False),
        }
    
    return {
        "language": "unknown",
        "confidence": 0.0,
        "is_reliable": False,
    }


def validate_language_code(
    client: translate.Client,
    language_code: str,
) -> bool:
    """
    Validate if a language code is supported by Google Translate.
    
    Args:
        client: Google Cloud Translation client.
        language_code: ISO 639-1 language code to validate.
    
    Returns:
        True if the language code is supported.
    """
    supported = get_supported_languages(client)
    supported_codes = {lang["language"] for lang in supported}
    return language_code in supported_codes
