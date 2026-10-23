from __future__ import annotations

from translation_client import get_translation_client
from translation_models import BatchTranslationResult, TranslationRequest, ensure_text_list, normalize_language_code


def batch_translate(
    texts: list[str],
    target_language: str,
    source_language: str | None = None,
    *,
    formality: str | None = None,
    context: str | None = None,
) -> list[str]:
    normalized_texts = ensure_text_list(texts)
    requests = [
        TranslationRequest(
            text=text,
            source_language=normalize_language_code(source_language),
            target_language=normalize_language_code(target_language) or "EN",
            formality=formality,
            context=context,
            model_type="quality_optimized",
        )
        for text in normalized_texts
    ]
    client = get_translation_client()
    results = client.translate_batch(requests)
    batch = BatchTranslationResult(items=results, provider="DeepL")
    return batch.texts()
