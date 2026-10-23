from __future__ import annotations

from typing import List

import deepl


DEFAULT_TARGET_LANGUAGE = "EN-US"


def translate_query(query: str, target_language: str = DEFAULT_TARGET_LANGUAGE) -> str:
    translator = deepl.Translator(auth_key=deepl.util.get_env_var("DEEPL_AUTH_KEY"))
    result = translator.translate_text(query, target_lang=target_language)
    return str(result)
