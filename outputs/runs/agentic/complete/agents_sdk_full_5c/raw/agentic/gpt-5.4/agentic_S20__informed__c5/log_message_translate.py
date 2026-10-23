from __future__ import annotations

import os
from typing import Optional

import deepl


DEEPL_MODEL_TYPE = "prefer_quality_optimized"


def log_message_translate(
    text: str,
    *,
    target_lang: str,
    source_lang: Optional[str] = None,
) -> str:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang,
        model_type=DEEPL_MODEL_TYPE,
    )
    return result.text
