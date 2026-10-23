"""
Translates a single text string between languages using Google Cloud Translation.
"""
from translation_client import get_translation_client

def translate_single_text(
    text: str, 
    target_language: str, 
    source_language: str = "en"
) -> str:
    """
    Translates a single string of text.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code of the language to translate to.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        The translated text.
    """
    client = get_translation_client()
    
    result = client.translate(
        values=text,
        target_language=target_language,
        source_language=source_language,
        format_="text"  # Explicitly set to text
    )
    
    return result['translatedText']
