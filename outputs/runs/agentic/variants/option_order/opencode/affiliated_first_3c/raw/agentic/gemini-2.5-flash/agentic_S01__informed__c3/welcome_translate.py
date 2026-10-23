import os
from google.cloud import translate_v2 as translate


def welcome_translate(text: str, target_language: str) -> str:
    translate_client = translate.Client()
    # Google Cloud Translation uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    # The client automatically picks up credentials from the environment.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
