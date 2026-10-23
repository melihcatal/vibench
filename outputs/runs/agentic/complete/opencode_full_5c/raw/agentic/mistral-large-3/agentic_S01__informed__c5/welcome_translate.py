import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate
from pydantic import BaseModel


class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: str = "en"


class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: str


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = translate.Client()
    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )
    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_source_language=result["detectedSourceLanguage"],
    )


def welcome_translate(text: str, target_language: str) -> str:
    request = TranslationRequest(text=text, target_language=target_language)
    response = translate_text(request)
    return response.translated_text
