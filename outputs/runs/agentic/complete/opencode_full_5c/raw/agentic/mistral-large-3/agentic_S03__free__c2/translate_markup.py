from typing import Optional
from bs4 import BeautifulSoup
from translation_client import TranslationClient
from translation_models import normalize_language_code


def translate_markup(
    markup: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """Translate HTML or markup while preserving tags using Google Cloud Translation API."""
    soup = BeautifulSoup(markup, "html.parser")
    client = TranslationClient()
    target_language = normalize_language_code(target_language)
    source_language = (
        normalize_language_code(source_language) if source_language else None
    )

    for element in soup.find_all(text=True):
        if element.parent.name not in ["script", "style"] and element.strip():
            translated_text = client.translate_text(
                str(element), target_language, source_language
            )
            element.replace_with(translated_text)

    return str(soup)
