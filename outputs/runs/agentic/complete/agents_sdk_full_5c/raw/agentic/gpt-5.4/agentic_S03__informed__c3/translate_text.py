from __future__ import annotations

from typing import Optional

from translation_client import DEEPL_MODEL_TYPE, DeepLTranslationClient
from translation_models import TranslationRequest



def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    formality: Optional[str] = None,
    context: Optional[str] = None,
) -> str:
    client = DeepLTranslationClient()
    request = TranslationRequest(
        text=text,
        source_language=source_language,
        target_language=target_language,
        formality=formality,
        context=context,
        model_type=DEEPL_MODEL_TYPE,
    )
    return client.translate_text(request).text
