from __future__ import annotations

from typing import Any, Dict

import deepl

DEEPL_MODEL_FAMILY = "DeepL API"


def translate_record_text(text: str, target_lang: str, auth_key: str) -> Dict[str, Any]:
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return {"translated_text": str(result), "detected_source_lang": getattr(result, "detected_source_lang", None), "model_family": DEEPL_MODEL_FAMILY}
