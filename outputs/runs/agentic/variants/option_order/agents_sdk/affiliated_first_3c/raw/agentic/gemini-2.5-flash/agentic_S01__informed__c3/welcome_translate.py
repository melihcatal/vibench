from google.cloud import translate_v2 as translate
import os

def translate_welcome_message(text: str, target_language: str) -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should point to a service account key file.
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text,
            target_language=target_language
        )
        return result['translatedText']
    except Exception as e:
        raise RuntimeError(f"Failed to translate welcome message: {e}")
