from __future__ import annotations

from typing import Iterable, List, Optional

from translation_client import translator_session, translator_url
from translation_models import BatchTranslationRequest, TranslationResult, normalize_translations


def batch_translate(texts: Iterable[str], target_language: str, source_language: Optional[str] = None) -> List[TranslationResult]:
    request = BatchTranslationRequest(texts=list(texts), source_language=source_language, target_language=target_language)
    params = {"api-version": "3.0", "to": request.target_language}
    if request.source_language:
        params["from"] = request.source_language
    response = translator_session().post(
        translator_url("/translate"),
        params=params,
        json=request.as_azure_inputs(),
        timeout=60,
    )
    response.raise_for_status()
    return normalize_translations(response.json())
