from typing import Optional, Dict, Any
from google.cloud import translate_v2 as translate
from model_client import get_llm_client


def translate_result(
    text: str, target_language: str = "es", source_language: Optional[str] = None
) -> str:
    """
    Translates generated model output using Google Cloud Translation API.

    Args:
        text: The input text to translate.
        target_language: The target language code for translation.
        source_language: The source language code (optional).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()

    result = translate_client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]
