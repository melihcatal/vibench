from __future__ import annotations

from typing import Optional

from translation_client import build_translation_client, normalize_translation_languages
from translation_models import TranslationRequest, TranslationResult, normalize_text


def translate_markup(
    markup: str,
    target_language: str,
    source_language: Optional[str] = None,
) -> TranslationResult:
    client, parent, model_path = build_translation_client()
    source_language, target_language = normalize_translation_languages(source_language, target_language)
    request = TranslationRequest(
        text=normalize_text(markup),
        source_language=source_language,
        target_language=target_language,
        mime_type="text/html",
    )
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "mime_type": request.mime_type,
            "target_language_code": request.target_language,
            "source_language_code": request.source_language,
            "model": model_path,
        }
    )
    item = response.translations[0]
    return TranslationResult(
        translated_text=item.translated_text,
        detected_language=getattr(item, "detected_language_code", None),
        provider="google-cloud-translate",
        model="general/nmt",
        raw=response,
    )
