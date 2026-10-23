from __future__ import annotations

import os

from deepL import Translator as _DeepLTranslator

DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"


def translate_compliance_note(text: str, target_lang: str = "EN-US") -> str:
    auth_key = os.environ.get(DEEPL_AUTH_KEY_ENV, "")
    translator = _DeepLTranslator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
