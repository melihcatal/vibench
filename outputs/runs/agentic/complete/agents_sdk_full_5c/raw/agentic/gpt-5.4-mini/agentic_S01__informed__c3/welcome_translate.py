from __future__ import annotations

from typing import Any, Dict

from deepl import Translator

from identity_models import normalize_locale, normalize_text

DEEPL_MODEL = "deepl-api"


def welcome_translate(text: str, target_locale: str) -> Dict[str, Any]:
    translator = Translator()
    source_text = normalize_text(text)
    locale = normalize_locale(target_locale)
    result = translator.translate_text(source_text, target_lang=locale.split("-")[0].upper())
    return {"provider": "DeepL API", "model": DEEPL_MODEL, "locale": locale, "translation": result.text}
