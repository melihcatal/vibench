from typing import List
from translation_client import get_translation_client


def batch_translate(
    texts: List[str], target_language: str, source_language: str = "en"
) -> List[str]:
    """
    Translates a list of text strings to a target language.

    Args:
        texts: A list of strings to translate.
        target_language: The target language code.
        source_language: The source language code.

    Returns:
        A list of translated strings, in the same order as the input.
    """
    client = get_translation_client()
    result = client.translate(
        texts, target_language=target_language, source_language=source_language
    )
    return [item["translatedText"] for item in result]
