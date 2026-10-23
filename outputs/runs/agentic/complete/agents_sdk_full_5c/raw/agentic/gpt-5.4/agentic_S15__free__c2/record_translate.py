from __future__ import annotations

import os
from typing import Iterable, List

import deepl


DEEPL_TARGET_LANG_ENV = "DEEPL_TARGET_LANG"


def translate_fields(text_fields: Iterable[str], target_lang: str | None = None) -> List[str]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    target = target_lang or os.getenv(DEEPL_TARGET_LANG_ENV, "EN-US")
    results = translator.translate_text(list(text_fields), target_lang=target)
    if not isinstance(results, list):
        results = [results]
    return [item.text for item in results]
