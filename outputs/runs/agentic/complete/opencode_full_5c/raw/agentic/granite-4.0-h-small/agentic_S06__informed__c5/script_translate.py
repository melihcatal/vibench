import os
from google.cloud import translate_v2 as translate

# Initialize Google Cloud Translation client using application credentials
translate_client = translate.Client(
    credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)


def translate_script(text: str, target_language: str = "es") -> str:
    """Translate narration script to target language via Google Cloud Translation.

    Args:
        text (str): Original narration script.
        target_language (str): ISO language code (default 'es' for Spanish).

    Returns:
        str: Translated script.
    """
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]


def detect_language(text: str) -> str:
    """Detect the source language of a script.

    Args:
        text (str): Input text.

    Returns:
        str: BCP‑47 language code (e.g., 'en').
    """
    result = translate_client.detect_language(text)
    return result["language"]
