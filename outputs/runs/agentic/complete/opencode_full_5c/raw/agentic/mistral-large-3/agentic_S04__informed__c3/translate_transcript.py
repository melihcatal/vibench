import os
from typing import List
import deepl
from speech_models import TranslationRequest, TranslationResponse


def translate_transcript(
    text: str, source_lang: str = "en", target_lang: str = "es"
) -> TranslationResponse:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(
        text, source_lang=source_lang, target_lang=target_lang
    )
    return TranslationResponse(translated_text=result.text)
