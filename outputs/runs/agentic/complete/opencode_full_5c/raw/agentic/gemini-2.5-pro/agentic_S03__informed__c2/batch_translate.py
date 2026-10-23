from typing import List
from translation_client import get_translation_client


def batch_translate(
    texts: List[str], target_language: str, source_language: str = "en"
) -> List[str]:
    """
    Translates a list of strings using Google Cloud Translation.
    """
    client = get_translation_client()
    results = client.translate(
        texts, target_language=target_language, source_language=source_language
    )
    return [result["translatedText"] for result in results]
