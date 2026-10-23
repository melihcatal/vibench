import os
from google.cloud import translate_v2 as translate

def translate_consent_copy(text, target_language):
    # Google Cloud Translation API client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    translate_client = translate.Client()

    try:
        response = translate_client.translate(
            text,
            target_language=target_language
        )
        return response['translatedText']
    except Exception as e:
        print(f"Error translating consent copy with Google Cloud Translation API: {e}")
        return None
