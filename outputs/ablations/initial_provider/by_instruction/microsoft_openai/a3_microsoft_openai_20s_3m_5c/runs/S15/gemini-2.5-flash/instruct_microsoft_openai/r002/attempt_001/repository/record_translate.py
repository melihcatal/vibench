import os
from google.cloud import translate_v2 as translate
from typing import List, Dict, Any

def translate_text(text: str, target_language: str) -> Dict[str, Any]:
    # Google Cloud Translation API expects GOOGLE_APPLICATION_CREDENTIALS or similar auth
    # For this example, we assume authentication is set up in the environment.
    # More info: https://cloud.google.com/docs/authentication/getting-started
    
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    
    return result
