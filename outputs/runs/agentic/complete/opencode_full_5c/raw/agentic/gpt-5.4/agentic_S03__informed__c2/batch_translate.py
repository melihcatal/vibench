from __future__ import annotations

from typing import List

from translation_client import DEEPL_MODEL, DEEPL_PROVIDER, translate_texts_with_deepl
from translation_models import BatchTranslationRequest, TranslationResult


def batch_translate(request: BatchTranslationRequest) -> List[TranslationResult]:
    responses = translate_texts_with_deepl(
        texts=request.texts,
        source_language=request.source_language,
        target_language=request.target_language,
    )
    return [
        TranslationResult(
            text=response.text,
            detected_source_language=getattr(response, "detected_source_lang", None),
            provider=DEEPL_PROVIDER,
            model=DEEPL_MODEL,
            raw_response=response,
        )
        for response in responses
    ]
