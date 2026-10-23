from __future__ import annotations

import os
from typing import Iterable, List

import deepl


DEEPL_TARGET_LANG_ENV = "DEEPL_TARGET_LANG"


def record_translate(text_fields: Iterable[str], target_lang: str | None = None) -> List[str]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    target = target_lang or os.environ.get(DEEPL_TARGET_LANG_ENV, "EN-US")
    outputs: List[str] = []
    for text in text_fields:
        if not text:
            outputs.append("")
            continue
        result = translator.translate_text(text, target_lang=target)
        outputs.append(result.text)
    return outputs
