# Federated Login Flow - Consent Translation

import os
from typing import Dict
from google.cloud import translate_v2 as translate


def consent_translate(text: str, target_language: str) -> str:
    """Translate identity-provider consent copy using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
