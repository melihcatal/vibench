from google.cloud import translate_v2 as translate
from typing import Optional


def translate_appeal_text(text: str, target_language: str = "en") -> Optional[str]:
    """
    Translates appeal text for review using Google Cloud Translation API.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result.get("translatedText")