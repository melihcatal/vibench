import os
from google.cloud import translate_v2 as translate


def welcome_translate(text: str, target_language: str = "es") -> str:
    """Translate onboarding copy into the user's locale using Google Cloud Translation."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    try:
        client = translate.Client()

        result = client.translate(text, target_language=target_language, model="nmt")

        return result["translatedText"]
    except Exception as e:
        raise Exception(f"Google Cloud Translation failed: {str(e)}")
