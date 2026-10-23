from typing import Dict, List
from bs4 import BeautifulSoup
from translation_client import GoogleTranslationClient
from translation_models import TranslationRequest, normalize_language_code


def translate_markup(
    markup: str, target_language: str, source_language: str = None
) -> str:
    soup = BeautifulSoup(markup, "html.parser")
    client = GoogleTranslationClient()
    target_language = normalize_language_code(target_language)
    source_language = (
        normalize_language_code(source_language) if source_language else None
    )

    for element in soup.find_all(text=True):
        if element.parent.name not in ["script", "style"] and element.strip():
            request = TranslationRequest(
                text=element,
                target_language=target_language,
                source_language=source_language,
                format_="html",
            )
            response = client.translate_text(request)
            element.replace_with(response.translated_text)

    return str(soup)
