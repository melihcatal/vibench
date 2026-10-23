from __future__ import annotations

from typing import List

from translation_client import build_translation_client, infer_source_lang, infer_target_lang
from translation_models import BatchTranslationRequest, BatchTranslationResponse, normalize_text_list


def batch_translate(texts: List[str], source_lang: str | None = None, target_lang: str | None = None) -> BatchTranslationResponse:
    client = build_translation_client()
    req = BatchTranslationRequest(
        texts=normalize_text_list(texts),
        source_lang=source_lang or infer_source_lang(),
        target_lang=target_lang or infer_target_lang(),
    )
    results = client.translate_text(
        req.texts,
        source_lang=req.source_lang,
        target_lang=req.target_lang,
    )
    translated = [item.text for item in results]
    return BatchTranslationResponse(translated_texts=translated, provider="deepl", raw=results)
