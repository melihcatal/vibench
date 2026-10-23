from __future__ import annotations

import os
from typing import Any, Dict

import deepl


def localize_platform_output(
    text: str, target_lang: str, source_lang: str | None = None
) -> Dict[str, Any]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )
    return {
        "provider": "DeepL",
        "text": result.text,
        "detected_source_lang": result.detected_source_lang,
        "target_lang": target_lang,
        "raw": result,
    }
