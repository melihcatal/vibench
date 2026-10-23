from typing import Dict, List, Optional
import os
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def translate_text(
    text: str,
    source_lang: str,
    target_lang: str,
    category: Optional[str] = None,
) -> str:
    """
    Translates a single text string between languages using Azure AI Translator.
    """
    client = get_translation_client()

    request = TranslationRequest(
        texts=[text],
        source_language=source_lang,
        target_languages=[target_lang],
        category=category,
    )

    response = client.translate(request)
    return response.translations[target_lang][0]
