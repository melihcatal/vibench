from __future__ import annotations

from typing import Optional

from translation_client import translator_session, translator_url
from translation_models import TranslationRequest, TranslationResult, normalize_translations


def translate_markup(markup: str, target_language: str, source_language: Optional[str] = None) -> TranslationResult:
    request = TranslationRequest(
        text=markup,
        source_language=source_language,
        target_language=target_language,
        content_type="text/html",
    )
    params = {"api-version": "3.0", "to": request.target_language, "textType": "html"}
    if request.source_language:
        params["from"] = request.source_language
    response = translator_session().post(
        translator_url("/translate"),
        params=params,
        json=[request.as_azure_input()],
        timeout=30,
    )
    response.raise_for_status()
    return normalize_translations(response.json())[0]
