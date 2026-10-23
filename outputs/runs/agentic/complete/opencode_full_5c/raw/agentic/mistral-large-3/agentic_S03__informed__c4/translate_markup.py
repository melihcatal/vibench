from google.cloud import translate_v2 as translate
from bs4 import BeautifulSoup
from typing import List, Tuple
import re

# Provider: Google Cloud Translation (v2)
# Model: google/cloud-translate-v2

def _extract_text_and_tags(html: str) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Extracts text and tags from HTML markup for translation.
    
    Args:
        html: The HTML markup to process.
        
    Returns:
        A tuple containing the extracted text and a list of tags with their positions.
    """
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    tags = []
    
    for tag in soup.find_all(True):
        if tag.name and tag.string and tag.string.strip():
            tags.append((tag.string.strip(), f"<{tag.name}>{{}}</{tag.name}>))
    
    return text, tags


def _reconstruct_html(translated_text: str, tags: List[Tuple[str, str]]) -> str:
    """
    Reconstructs HTML markup with translated text while preserving tags.
    
    Args:
        translated_text: The translated text.
        tags: The list of tags and their positions.
        
    Returns:
        The reconstructed HTML markup.
    """
    for original, tag_pattern in tags:
        translated_text = translated_text.replace(original, tag_pattern, 1)
    
    # Replace placeholders with actual tags
    translated_text = re.sub(r'<(\w+)>\{\}</\1>', r'{\1}', translated_text)
    for tag in set(re.findall(r'{\w+}', translated_text)):
        tag_name = tag[1:-1]
        translated_text = translated_text.replace(tag, f'<{tag_name}></{tag_name}>')
    
    return translated_text


def translate_markup(markup: str, target_language: str, source_language: str = None) -> str:
    """
    Translates HTML or markup while preserving tags using Google Cloud Translation.
    
    Args:
        markup: The HTML or markup to translate.
        target_language: The target language code (e.g., 'es', 'fr').
        source_language: The source language code (optional, e.g., 'en').
        
    Returns:
        The translated markup with tags preserved.
    """
    if not markup:
        return markup

    text, tags = _extract_text_and_tags(markup)
    client = translate.Client()
    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )
    return _reconstruct_html(result['translatedText'], tags)