import os
import deepl
from speech_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)

    result = translator.translate_text(request.text, target_lang=request.target_lang)

    return TranslationResponse(translated_text=result.text)
