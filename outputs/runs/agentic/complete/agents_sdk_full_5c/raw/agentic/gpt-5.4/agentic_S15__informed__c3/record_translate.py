from __future__ import annotations

import os
from typing import Any, Dict, Iterable, Mapping

import deepl



def translate_text(text: str, target_language: str, source_language: str | None = None) -> Dict[str, Any]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_language, source_lang=source_language)
    return {
        "provider": "DeepL API",
        "text": result.text,
        "detected_source_language": getattr(result, "detected_source_lang", source_language),
        "target_language": target_language,
    }



def translate_record_fields(record: Mapping[str, Any], fields: Iterable[str], target_language: str, source_language: str | None = None) -> Dict[str, Any]:
    translated: Dict[str, Any] = dict(record)
    translations: Dict[str, Any] = {}
    for field in fields:
        value = record.get(field)
        if isinstance(value, str) and value.strip():
            payload = translate_text(value, target_language=target_language, source_language=source_language)
            translated[field] = payload["text"]
            translations[field] = payload
    return {"record": translated, "translations": translations}
