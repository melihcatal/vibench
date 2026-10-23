from typing import Optional, List
from bs4 import BeautifulSoup
from translation_client import TranslationClient
from translation_models import normalize_language_code


def translate_markup(
    markup: str,
    target_language: str,
    source_language: Optional[str] = None,
    protected_tags: Optional[List[str]] = None,
) -> str:
    if protected_tags is None:
        protected_tags = []

    soup = BeautifulSoup(markup, "html.parser")
    text_elements = []

    for element in soup.find_all(text=True):
        if element.parent.name not in protected_tags and element.strip():
            text_elements.append((element, element.string))

    texts = [text for _, text in text_elements]
    if not texts:
        return markup

    client = TranslationClient()
    normalized_target = normalize_language_code(target_language)
    normalized_source = (
        normalize_language_code(source_language) if source_language else None
    )
    translations = client.batch_translate_text(
        texts, normalized_target, normalized_source
    )

    for (element, _), translation in zip(text_elements, translations):
        element.string.replace_with(translation)

    return str(soup)
