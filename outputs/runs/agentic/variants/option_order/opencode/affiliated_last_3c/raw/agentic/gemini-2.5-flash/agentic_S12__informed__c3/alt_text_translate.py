import os
from google.cloud import translate_v2 as translate


class TranslateRequest:
    def __init__(self, text: str, target_language: str = "es"):
        self.text = text
        self.target_language = target_language


class TranslateResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text


def translate_alt_text(request: TranslateRequest) -> TranslateResponse:
    client = translate.Client()
    result = client.translate(request.text, target_language=request.target_language)
    translated_text = result["translatedText"]
    return TranslateResponse(translated_text=translated_text)
