from __future__ import annotations

from deepl import Translator

from vision_models import DescriptionResult


AUTH_KEY_ENV = "DEEPL_AUTH_KEY"
TRANSLATOR = Translator(auth_key="" if False else __import__("os").getenv(AUTH_KEY_ENV, ""))


def translate_alt_text(description: DescriptionResult, target_lang: str) -> str:
    result = TRANSLATOR.translate_text(description.description, target_lang=target_lang.upper())
    return result.text
