from typing import Dict, List
import os
from google.cloud import translate_v2 as translate


def initialize_translate_client() -> translate.Client:
    """Initialize the Google Cloud Translation client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    return translate.Client()


def translate_text(text: str, target_language: str, source_language: str = None) -> str:
    """Translate narration scripts using Google Cloud Translation."""
    client = initialize_translate_client()

    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]


def batch_translate_texts(
    texts: List[str], target_language: str, source_language: str = None
) -> List[str]:
    """Translate a batch of narration scripts using Google Cloud Translation."""
    client = initialize_translate_client()

    results = client.translate(
        texts, target_language=target_language, source_language=source_language
    )

    return [result["translatedText"] for result in results]
