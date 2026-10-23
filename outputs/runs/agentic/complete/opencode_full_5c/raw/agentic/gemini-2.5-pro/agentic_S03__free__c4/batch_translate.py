from typing import List
from translation_client import get_translation_client


def batch_translate_text(
    texts: List[str], target_language: str, source_language: str = None
):
    """
    Translates a list of text strings.

    Args:
        texts: A list of strings to translate.
        target_language: The language to translate the text into.
        source_language: The source language of the text. If None, the API will
                         attempt to detect the source language for each string.

    Returns:
        A list of dictionaries, where each dictionary contains the translated
        text and detected source language for the corresponding input string.
    """
    client = get_translation_client()
    result = client.translate(
        texts,
        target_language=target_language,
        source_language=source_language if source_language else "",
    )
    return result
