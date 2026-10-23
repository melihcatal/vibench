from __future__ import annotations

from translation_client import get_deepl_client
from translation_models import TranslationRequest


def translate_dictionary_values(
    values_by_key: dict[str, str],
    source_language: str,
    target_language: str,
    formality: str | None = None,
) -> dict[str, str]:
    keys = list(values_by_key.keys())
    texts = [values_by_key[key] for key in keys]
    request = TranslationRequest(
        text="",
        source_language=source_language,
        target_language=target_language,
        formality=formality,
    )
    translator = get_deepl_client()
    results = translator.translate_text(texts, **request.to_deepl_kwargs())
    return {key: result.text for key, result in zip(keys, results)}
