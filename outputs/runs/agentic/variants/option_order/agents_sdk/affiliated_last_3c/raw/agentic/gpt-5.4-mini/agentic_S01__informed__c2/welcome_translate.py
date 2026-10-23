from __future__ import annotations

from typing import Dict

import deepl

from identity_models import normalize_locale

DEEPL_MODEL_SIGNAL = "deepl"


def welcome_translate(text: str, target_locale: str) -> Dict[str, str]:
    translator = deepl.Translator(auth_key=__import__("os").environ.get("DEEPL_AUTH_KEY", ""))
    target_lang = normalize_locale(target_locale).split("-")[0].upper()
    result = translator.translate_text(text, target_lang=target_lang)
    return {"translated_text": str(result), "target_locale": normalize_locale(target_locale), "provider": DEEPL_MODEL_SIGNAL}
