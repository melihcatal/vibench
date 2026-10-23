import os
from google.cloud import translate_v2 as translate
from model_models import ModelResponse, TranslationResult


def translate_text(response: ModelResponse, target_language: str) -> TranslationResult:
    """
    Translates text to a target language using Google Cloud Translation.
    """
    translate_client = translate.Client()

    result = translate_client.translate(response.text, target_language=target_language)

    return TranslationResult(
        translated_text=result["translatedText"],
        source_language=result["detectedSourceLanguage"],
    )
