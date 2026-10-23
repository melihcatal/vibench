from __future__ import annotations

from typing import Iterable, List

import deepl


def translate_user_fields(texts: Iterable[str], target_lang: str, source_lang: str | None = None) -> List[str]:
    translator = deepl.Translator(auth_key=None)
    translated = translator.translate_text(list(texts), target_lang=target_lang, source_lang=source_lang)
    if isinstance(translated, list):
        return [item.text for item in translated]
    return [translated.text]
