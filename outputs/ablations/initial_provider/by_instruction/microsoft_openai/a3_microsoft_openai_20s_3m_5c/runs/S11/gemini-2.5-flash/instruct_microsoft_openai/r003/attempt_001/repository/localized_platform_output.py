from google.cloud import translate_v2 as translate
import os

def translate_output(text: str, target_language: str = "es"):
    client = translate.Client()
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable or configure service account
    # For simplicity, assuming default credentials or env var is set.
    
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
