from __future__ import annotations

from typing import List
import os

import deepl


def log_message_translate(
    messages: List[str], target_lang: str, source_lang: str | None = None
) -> List[str]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    results = translator.translate_text(
        messages, target_lang=target_lang, source_lang=source_lang
    )
    if isinstance(results, list):
        return [item.text for item in results]
    return [results.text]
