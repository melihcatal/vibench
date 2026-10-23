"""
Translates a list of strings while preserving order using Google Cloud Translation.
"""
from typing import List
from translation_client import get_translation_client

def translate_text_batch(
    texts: List[str], 
    target_language: str, 
    source_language: str = "en"
) -> List[str]:
    """
    Translates a batch of text strings.

    Args:
        texts: A list of texts to translate.
        target_language: The ISO 639-1 code of the language to translate to.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        A list of translated texts, in the same order as the input.
    """
    if not texts:
        return []

    client = get_translation_client()
    
    results = client.translate(
        values=texts,
        target_language=target_language,
        source_language=source_language
    )
    
    return [result['translatedText'] for result in results]
