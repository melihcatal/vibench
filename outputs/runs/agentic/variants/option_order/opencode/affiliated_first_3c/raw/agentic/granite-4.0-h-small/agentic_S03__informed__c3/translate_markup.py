from bs4 import BeautifulSoup
from translation_client import normalize_request, normalize_response
from translation_models import TranslationRequest, TranslationResponse
from translation_client import get_translation_service_client


def translate_markup(
    text: str, source_lang: str, target_lang: str, provider: str = "deepl"
) -> str:
    """
    Translate HTML/markup content while preserving tags and structure.
    The function extracts tag contents, translates them, then re‑writes the full markup.

    Args:
        text: Raw HTML/markup string (e.g., "<p>Hello world</p>").
        source_lang: ISO 639‑1 source language code.
        target_lang: ISO 639‑1 target language code.
        provider: Translation provider identifier.

    Returns:
        Translated HTML/markup with the same tags and hierarchy.
    """
    soup = BeautifulSoup(text, "html.parser")

    def translate_tag(element):
        # Translate navigable strings only; leave tags and attributes untouched.
        for child in element.find_all(string=True):
            text_content = child.strip()
            if not text_content:
                continue
            payload = {
                "text": text_content,
                "source": source_lang,
                "target": target_lang,
            }
            resp = client.translate_text(
                **normalize_request(TranslationRequest(**payload), provider)
            )
            translated = normalize_response(resp, provider)["translated_text"]
            # Replace the original string with the translated one, preserving whitespace.
            child.replace_with(translated)
        # Recurse into nested tags.
        for tag in element.find_all(True):
            translate_tag(tag)

    # Start with top‑level parsed root.
    translate_tag(soup)
    return str(soup)


# Helper client instance (can be reused across calls if desired)
global client
client = get_translation_service_client("deepl")  # default, change as needed
