from typing import Optional
from bs4 import BeautifulSoup
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def translate_markup(
    markup: str,
    source_lang: str,
    target_lang: str,
    category: Optional[str] = None,
) -> str:
    """
    Translates HTML or markup while preserving tags using Azure AI Translator.
    """
    soup = BeautifulSoup(markup, "html.parser")
    text_blocks = []

    for element in soup.find_all(text=True):
        if element.parent.name not in ["script", "style"] and element.strip():
            text_blocks.append((element, element.string))

    texts = [text for _, text in text_blocks]
    if not texts:
        return markup

    client = get_translation_client()
    request = TranslationRequest(
        texts=texts,
        source_language=source_lang,
        target_languages=[target_lang],
        category=category,
    )

    response = client.translate(request)
    translated_texts = response.translations[target_lang]

    for (element, _), translated_text in zip(text_blocks, translated_texts):
        element.string.replace_with(translated_text)

    return str(soup)
