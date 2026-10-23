import os
from deepl import Translator
from security_models import TranslationRequest, TranslationResponse


def runbook_translate(
    text: str, target_language: str, source_language: str = None
) -> TranslationResponse:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))

    result = translator.translate_text(
        text=text, target_lang=target_language, source_lang=source_language
    )

    return TranslationResponse(
        translated_text=result.text, detected_language=result.detected_source_lang
    )
