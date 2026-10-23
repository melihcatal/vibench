import os
from typing import Optional, List
from google.cloud import translate_v2 as translate

from identity_client import GOOGLE_CLOUD_PROJECT_ID

def translate_consent_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    """Translates identity-provider consent copy using Google Cloud Translation AI."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # or pass credentials directly if needed.
    # For this example, we assume GOOGLE_APPLICATION_CREDENTIALS is set.

    translate_client = translate.Client(project=GOOGLE_CLOUD_PROJECT_ID)

    # Text can also be a list of strings, in which case a list of translations is returned.
    # Here we handle a single string.
    result = translate_client.translate(text, target_language=target_language, source_language=source_language)
    
    return result['translatedText']
