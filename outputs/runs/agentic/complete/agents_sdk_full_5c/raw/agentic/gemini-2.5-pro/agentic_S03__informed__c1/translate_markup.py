"""
Translates HTML or markup while preserving tags using Google Cloud Translation.
"""
from translation_client import get_translation_client

def translate_html_content(
    html_content: str, 
    target_language: str, 
    source_language: str = "en"
) -> str:
    """
    Translates HTML content, preserving the markup structure.

    Args:
        html_content: The HTML content string to translate.
        target_language: The ISO 639-1 code of the language to translate to.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        The translated HTML content as a string.
    """
    client = get_translation_client()
    
    result = client.translate(
        values=html_content,
        target_language=target_language,
        source_language=source_language,
        format_='html'
    )
    
    return result['translatedText']
