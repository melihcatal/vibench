import os
from google.cloud import translate_v2 as translate
from .speech_models import TranslationRequest, TranslationResponse


def translate_transcript(text: str, target_language: str) -> TranslationResponse:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return TranslationResponse(translated_text=result["translatedText"])
