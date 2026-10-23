import os

# Google Cloud Translation client helper utilities
from google.cloud import translate_v2 as translate

# Export the client for reuse across modules
translate_client = translate.Client()

# Configuration loading
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Request/response normalization helpers

def normalize_response(response):
    """Extract translated text from raw API response."""
    return response["translatedText"] if isinstance(response, dict) else response

# Utility to ensure string inputs

def ensure_string(value):
    return value if isinstance(value, str) else str(value)
