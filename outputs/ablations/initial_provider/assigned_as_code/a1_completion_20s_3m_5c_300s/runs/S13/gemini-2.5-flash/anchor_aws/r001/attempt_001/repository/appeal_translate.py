import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate

def appeal_translate(text: str, target_language: str, config: Dict[str, Any] = None) -> str:
    config = config or {}
    
    # Initialize Google Cloud Translation client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or authenticated otherwise
    client = translate.Client()

    # The text to translate
    translation_response = client.translate(text, target_language=target_language)

    return translation_response["translatedText"]
