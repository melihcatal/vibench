from typing import List, Dict, Any

class TranslationRequest:
    def __init__(self, text: str, target_language: str, source_language: str = "auto"):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language

class TranslationResponse:
    def __init__(self, translated_text: str, detected_source_language: str):
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language
