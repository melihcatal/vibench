import os
from typing import Union
from deepl import Translator
from security_models import TranslationResult


def translate_compliance_note(
    text: Union[str, bytes], target_language: str = "EN-US"
) -> TranslationResult:
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    translator = Translator(auth_key=os.getenv("DEEPL_AUTH_KEY"))

    result = translator.translate_text(text, target_lang=target_language)

    return TranslationResult(
        translated_text=result.text,
        source_language=translator.detect_language(text).language,
        target_language=target_language,
    )
