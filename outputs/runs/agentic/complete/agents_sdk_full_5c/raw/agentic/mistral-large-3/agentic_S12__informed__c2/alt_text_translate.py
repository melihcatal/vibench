import os
from google.cloud import translate_v2 as translate
from vision_models import TranslationResult

class GoogleTranslateClient:
    def __init__(self):
        self.client = translate.Client()

    def translate_text(self, text: str, target_language: str) -> TranslationResult:
        result = self.client.translate(text, target_language=target_language)
        return TranslationResult(
            translated_text=result["translatedText"],
            source_language=result["detectedSourceLanguage"],
            target_language=target_language
        )

def translate_alt_text(text: str, target_language: str) -> TranslationResult:
    translator = GoogleTranslateClient()
    return translator.translate_text(text, target_language)