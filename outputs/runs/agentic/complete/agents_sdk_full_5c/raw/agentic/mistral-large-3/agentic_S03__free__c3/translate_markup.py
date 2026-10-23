from typing import Optional
from bs4 import BeautifulSoup
from translation_client import get_translation_client
from translate_text import translate_text

def translate_markup(
    markup: str,
    source_lang: str,
    target_lang: str,
    model: str = "google-translate-v3",
    glossary_id: Optional[str] = None,
) -> str:
    """Translate HTML or markup while preserving tags using Google Cloud Translation API."""
    soup = BeautifulSoup(markup, "html.parser")
    for string in soup.stripped_strings:
        translated = translate_text(
            text=str(string),
            source_lang=source_lang,
            target_lang=target_lang,
            model=model,
            glossary_id=glossary_id,
        )
        string.replace_with(translated)
    return str(soup)