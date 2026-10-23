"""
translation_client.py - Provide local configuration and client helper utilities
for General Text Translation using Google Cloud Translation API v3.
"""

import os
from typing import List, Optional, Dict, Any
from google.cloud import translate_v3 as translate
from google.api_core.client_options import ClientOptions

GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
TRANSLATION_API_ENDPOINT = "translate.googleapis.com"


def get_translation_client() -> translate.TranslationServiceClient:
    """
    Create and return a Google Cloud Translation v3 client.
    Uses Application Default Credentials when GOOGLE_APPLICATION_CREDENTIALS
    environment variable points to a service account JSON key file.
    """
    options = ClientOptions(
        api_endpoint=TRANSLATION_API_ENDPOINT
    )
    client = translate.TranslationServiceClient(
        client_options=options
    )
    return client


def get_project_location() -> str:
    """Return the Google Cloud project location string for Translation API."""
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    project = GOOGLE_CLOUD_PROJECT or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    return f"projects/{project}/locations/{location}"


def build_glossary_id(glossary_name: str) -> Optional[str]:
    """Build a glossary resource ID for Google Cloud Translation."""
    if not GOOGLE_CLOUD_PROJECT:
        return None
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    return (
        f"projects/{GOOGLE_CLOUD_PROJECT}/locations/{location}"
        f"/glossaries/{glossary_name}"
    )


def load_credentials_from_env() -> bool:
    """Check if Google Cloud credentials are available."""
    if GOOGLE_APPLICATION_CREDENTIALS:
        return os.path.exists(GOOGLE_APPLICATION_CREDENTIALS)
    # Check for Application Default Credentials
    default_path = os.path.expanduser(
        "~/.config/gcloud/application_default_credentials.json"
    )
    return os.path.exists(default_path)


def validate_client_ready() -> bool:
    """Validate that the Google Cloud Translation client can be initialized."""
    return bool(GOOGLE_CLOUD_PROJECT and load_credentials_from_env())
