import os
from google.cloud import translate_v2 as translate


def translate_caption(text: str, target_language: str = "es") -> str:
    """Translates text using Google Cloud Translation."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print(
            "WARNING: GOOGLE_APPLICATION_CREDENTIALS not set. Relying on default application credentials."
        )

    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
