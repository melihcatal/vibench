import os
from typing import Optional
from bs4 import BeautifulSoup
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

def translate_markup(
    markup: str,
    source_lang: str,
    target_lang: str,
    model: str = "google-translate-ai-v3",
    glossary_id: Optional[str] = None,
) -> str:
    """Translate HTML or markup while preserving tags using Google Cloud Translation API."""
    soup = BeautifulSoup(markup, "html.parser")
    text_nodes = []
    for string in soup.stripped_strings:
        text_nodes.append(string)

    client = get_translation_client()
    request = TranslationRequest(
        text="\n".join(text_nodes),
        source_lang=source_lang,
        target_lang=target_lang,
        model=model,
        glossary_id=glossary_id,
        format_="html",
    )
    response = client.translate_text(request)
    translated_text = TranslationResponse(**response).translated_text

    translated_nodes = translated_text.split("\n")
    for idx, string in enumerate(soup.stripped_strings):
        if idx < len(translated_nodes):
            string.replace_with(translated_nodes[idx])

    return str(soup)