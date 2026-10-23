import os
from typing import Optional
from deepl import Translator
from pydantic import BaseModel


class TranslationRequest(BaseModel):
    text: str
    target_lang: str = "DE"
    source_lang: Optional[str] = None


class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_lang: str


def translate_result(
    text: str,
    target_lang: str = "DE",
    source_lang: Optional[str] = None
) -> TranslationResponse:
    """
    Translate generated model output using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")
    
    translator = Translator(auth_key=auth_key)
    result = translator.translate_text(
        text=text,
        target_lang=target_lang,
        source_lang=source_lang
    )
    
    return TranslationResponse(
        translated_text=result.text,
        detected_source_lang=result.detected_source_lang
    )