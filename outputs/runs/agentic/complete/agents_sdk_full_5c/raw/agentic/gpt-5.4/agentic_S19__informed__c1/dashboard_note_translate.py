from __future__ import annotations

import os
from typing import Any, Dict

import deepl


DEEPL_MODEL_TYPE = "quality_optimized"



def dashboard_note_translate(text: str, target_lang: str, source_lang: str | None = None) -> Dict[str, Any]:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang,
        model_type=DEEPL_MODEL_TYPE,
    )
    return {
        "provider": "DeepL API",
        "model_type": DEEPL_MODEL_TYPE,
        "text": result.text,
        "detected_source_lang": result.detected_source_lang,
        "target_lang": target_lang,
    }
