from google.cloud import translate_v2 as translate # Google Cloud provider-specific import
from typing import NamedTuple

class TranslationRequest(NamedTuple):
    text: str
    target_language: str

class TranslationResponse(NamedTuple):
    translated_text: str

def translate_script(request: TranslationRequest) -> TranslationResponse:
    """
    Translates narration scripts using Google Cloud Translation.
    """
    translate_client = translate.Client()

    result = translate_client.translate(
        request.text,
        target_language=request.target_language # Google Cloud provider-specific parameter
    )

    return TranslationResponse(translated_text=result['translatedText'])
