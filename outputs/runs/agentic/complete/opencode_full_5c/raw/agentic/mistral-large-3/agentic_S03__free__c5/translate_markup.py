from translation_client import TranslationClient
from translation_models import (
    MarkupTranslationRequest,
    extract_text_from_html,
    reconstruct_html_with_translations,
)
import os


def translate_markup(
    markup: str, target_language: str, source_language: str = None
) -> str:
    """
    Translates HTML or markup while preserving tags using Google Cloud Translation API.
    """
    client = TranslationClient(os.getenv("GOOGLE_CLOUD_PROJECT_ID"))
    request = MarkupTranslationRequest(
        markup=markup, target_language=target_language, source_language=source_language
    )

    texts = extract_text_from_html(request.markup)
    translations = []

    for text in texts:
        translated = client.translate_text(
            text, request.target_language, request.source_language
        )
        translations.append(translated)

    return reconstruct_html_with_translations(request.markup, translations)
