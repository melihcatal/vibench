import os
from google.cloud import translate_v2 as translate

def translate_payload(text_payload: str, target_language: str = "es") -> str:
    client = translate.Client()
    
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
    # For local development, you might need to run `gcloud auth application-default login`

    result = client.translate(text_payload, target_language=target_language)
    translated_text = result["translatedText"]
    
    return translated_text
