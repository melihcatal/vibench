import os
import deepl
from speech_models import TranslationRequest, TranslationResponse


def translate_script(request: TranslationRequest) -> TranslationResponse:
    """Translates a script using the DeepL API."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(request.text, target_lang=request.target_lang)

    return TranslationResponse(
        translated_text=result.text, detected_source_lang=result.detected_source_lang
    )
