import os
from google.cloud import translate_v2 as translate
from observability_models import TranslationRequest, TranslatedText


def translate_dashboard_note(request: TranslationRequest) -> TranslatedText:
    """
    Translates text using the Google Cloud Translation API.
    """
    client = translate.Client()

    result = client.translate(request.text, target_language=request.target_language)

    return TranslatedText(
        original_text=request.text,
        translated_text=result["translatedText"],
        target_language=request.target_language,
    )
