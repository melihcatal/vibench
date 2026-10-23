from __future__ import annotations

from typing import Iterable, List
import os

import deepl


def translate_log_messages(
    messages: Iterable[str], target_lang: str, source_lang: str | None = None
) -> List[str]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    results = translator.translate_text(
        list(messages), target_lang=target_lang, source_lang=source_lang
    )
    if not isinstance(results, list):
        results = [results]
    return [item.text for item in results]
