from __future__ import annotations

from translation_client import translate_texts as deepl_translate_texts
from translation_models import BatchTranslationRequest, BatchTranslationResponse, normalize_text_list


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    translated_texts = deepl_translate_texts(
        normalize_text_list(request.texts),
        request.source_language,
        request.target_language,
    )
    return BatchTranslationResponse(translated_texts=translated_texts)
