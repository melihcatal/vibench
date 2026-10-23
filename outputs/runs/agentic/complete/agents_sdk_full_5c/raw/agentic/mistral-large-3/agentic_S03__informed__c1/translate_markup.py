from typing import List, Tuple
from bs4 import BeautifulSoup
from translation_client import AmazonTranslateClient
from translation_models import normalize_language_code


def extract_text_and_tags(html: str) -> Tuple[List[str], List[str]]:
    """Extract text segments and their surrounding tags from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    text_segments = []
    tag_segments = []
    
    for element in soup.find_all(text=True):
        if element.parent.name not in ['script', 'style'] and element.strip():
            text_segments.append(element.strip())
            tag_segments.append(str(element.parent))
    
    return text_segments, tag_segments


def reconstruct_html(text_segments: List[str], tag_segments: List[str]) -> str:
    """Reconstruct HTML with translated text segments."""
    soup = BeautifulSoup('<div></div>', 'html.parser')
    div = soup.div
    
    for text, tag in zip(text_segments, tag_segments):
        new_tag = BeautifulSoup(tag, 'html.parser').find()
        if new_tag:
            new_tag.string = text
            div.append(new_tag)
    
    return str(div)


def translate_markup(html: str, source_lang: str, target_lang: str) -> str:
    """Translate HTML or markup while preserving tags using Amazon Translate."""
    client = AmazonTranslateClient()
    source_lang = normalize_language_code(source_lang)
    target_lang = normalize_language_code(target_lang)
    
    text_segments, tag_segments = extract_text_and_tags(html)
    translated_segments = []
    
    for segment in text_segments:
        translated_text = client.translate_text(segment, source_lang, target_lang)
        translated_segments.append(translated_text if translated_text else segment)
    
    return reconstruct_html(translated_segments, tag_segments)