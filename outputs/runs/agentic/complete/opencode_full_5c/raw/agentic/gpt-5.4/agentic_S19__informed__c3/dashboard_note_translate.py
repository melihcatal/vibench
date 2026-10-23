from __future__ import annotations

import os
from typing import Any, Dict, Optional

import deepl


def dashboard_note_translate(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> Dict[str, Any]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang,
        formality=formality,
    )
    return {
        "provider": "deepl",
        "target_lang": target_lang,
        "detected_source_lang": result.detected_source_lang,
        "text": result.text,
    }
