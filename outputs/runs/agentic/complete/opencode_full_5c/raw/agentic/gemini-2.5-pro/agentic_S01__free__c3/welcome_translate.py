import os
from google.cloud import translate_v2 as translate
from identity_models import TranslationRequest, TranslationResponse


def translate_welcome_message(request: TranslationRequest) -> TranslationResponse:
    """Translates text into the target language."""
    translate_client = translate.Client()

    if isinstance(request.text, bytes):
        text = request.text.decode("utf-8")
    else:
        text = request.text

    result = translate_client.translate(text, target_language=request.target_language)

    return TranslationResponse(translated_text=result["translatedText"])
