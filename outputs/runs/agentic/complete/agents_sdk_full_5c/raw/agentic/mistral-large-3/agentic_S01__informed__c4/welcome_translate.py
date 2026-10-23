import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any

class WelcomeTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_welcome_message(self, text: str, target_language: str) -> Dict[str, Any]:
        result = self.client.translate(text, target_language=target_language)
        return {
            "translated_text": result["translatedText"],
            "detected_source_language": result["detectedSourceLanguage"],
            "input_text": text
        }