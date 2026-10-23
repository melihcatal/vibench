import os
from google.cloud import translate_v2 as translate

def welcome_translate(text: str, target_language: str) -> str:
    client = translate.Client()
    
    # Google Cloud Translation API requires GOOGLE_APPLICATION_CREDENTIALS to be set
    # or running in a Google Cloud environment.
    # For local development, ensure your environment is authenticated.

    try:
        result = client.translate(
            text,
            target_language=target_language
        )
        return result['translatedText']
    except Exception as e:
        return f"Translation failed: {e}"
