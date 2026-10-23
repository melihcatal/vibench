import os
from typing import Dict
from google.cloud import translate_v2 as translate
from pydantic import BaseModel


class TranslatedOutput(BaseModel):
    translated_text: str
    source_language: str
    target_language: str


def translate_output(text: str, target_language: str) -> TranslatedOutput:
    """
    Translates platform model output to another locale using Google Cloud Translation.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_language)

    return TranslatedOutput(
        translated_text=result["translatedText"],
        source_language=result["detectedSourceLanguage"],
        target_language=target_language
    )