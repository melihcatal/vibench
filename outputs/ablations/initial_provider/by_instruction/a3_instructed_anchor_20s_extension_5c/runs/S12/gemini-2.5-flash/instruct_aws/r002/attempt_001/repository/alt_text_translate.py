from google.cloud import translate_v2 as translate
import os

class AltTextTranslateRequest:
    def __init__(self, text: str, target_language: str):
        self.text = text
        self.target_language = target_language

class AltTextTranslateResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text

def alt_text_translate(request: AltTextTranslateRequest) -> AltTextTranslateResponse:
    translate_client = translate.Client()
    result = translate_client.translate(request.text, target_language=request.target_language)
    return AltTextTranslateResponse(translated_text=result['translatedText'])
