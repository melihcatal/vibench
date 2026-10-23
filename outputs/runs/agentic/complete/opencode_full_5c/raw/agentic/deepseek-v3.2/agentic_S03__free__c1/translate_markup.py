import os
import re
from translation_client import get_translation_client
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse


def translate_markup(
    html_content: str, source_lang: str = "auto", target_lang: str = "en"
) -> str:
    """Translate HTML or markup while preserving tags using Google Cloud Translation API."""
    client = get_translation_client()

    if not html_content or not html_content.strip():
        return html_content

    try:
        from google.cloud import translate_v2 as translate

        result = client.translate(
            html_content,
            source_language=source_lang if source_lang != "auto" else None,
            target_language=target_lang,
            format_="html",
            model="nmt",
        )

        return result["translatedText"]
    except Exception as e:
        print(f"Markup translation error: {e}")
        return html_content
