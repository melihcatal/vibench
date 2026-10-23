# Local configuration and client helper utilities for Text Content Safety
import os
from typing import Optional
from google.cloud import language_v1
from google.api_core.client_options import ClientOptions


def get_perspective_client() -> language_v1.LanguageServiceClient:
    """Initialize Google Perspective API client."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    client_options = ClientOptions(api_key=api_key)
    return language_v1.LanguageServiceClient(client_options=client_options)


def get_client_config() -> dict:
    """Load provider-specific configuration."""
    return {
        "perspective": {
            "api_key": os.getenv("PERSPECTIVE_API_KEY"),
            "model": "latest",
            "host": "https://commentanalyzer.googleapis.com"
        }
    }


def get_default_thresholds() -> dict:
    """Default category thresholds for moderation."""
    return {
        "hate": 0.7,
        "violence": 0.8,
        "sexual": 0.6,
        "self_harm": 0.9,
        "harassment": 0.7,
        "dangerous": 0.8
    }