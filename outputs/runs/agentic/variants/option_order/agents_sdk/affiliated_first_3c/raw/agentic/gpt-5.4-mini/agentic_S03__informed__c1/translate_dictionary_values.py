from __future__ import annotations

from typing import Any, Mapping

from translation_client import build_translation_client, infer_source_lang, infer_target_lang
from translation_models import DictionaryTranslationRequest, preserve_key_order, normalize_text


def translate_dictionary_values(values: Mapping[str, Any], source_lang: str | None = None, target_lang: str | None = None) -> dict[str, str]:
    client = build_translation_client()
    req = DictionaryTranslationRequest(
        values=preserve_key_order(values),
        source_lang=source_lang or infer_source_lang(),
        target_lang=target_lang or infer_target_lang(),
    )
    translated: dict[str, str] = {}
    for key, value in req.values.items():
        result = client.translate_text(
            normalize_text(value),
            source_lang=req.source_lang,
            target_lang=req.target_lang,
        )
        translated[key] = result.text
    return translated
