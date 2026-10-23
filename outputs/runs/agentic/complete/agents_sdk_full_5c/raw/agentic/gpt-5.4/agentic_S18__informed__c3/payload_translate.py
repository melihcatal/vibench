from __future__ import annotations

from typing import Any, Dict
import os

import deepl

from messaging_models import extract_text_fields, normalize_payload



def translate_payload_text(payload: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    normalized = normalize_payload(payload)
    source_text = extract_text_fields(normalized)
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(source_text, target_lang=target_language.upper())
    translated_payload = dict(normalized)
    translated_payload["translated_text"] = result.text
    return {
        "provider": "DeepL API",
        "target_language": target_language.upper(),
        "detected_source_language": result.detected_source_lang,
        "payload": translated_payload,
    }
