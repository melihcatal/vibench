from typing import List, Dict, Union

class TranslationRequest:
    def __init__(self, texts: List[str], target_language: str, source_language: str = None, mime_type: str = "text/plain"):
        self.texts = texts
        self.target_language = target_language
        self.source_language = source_language
        self.mime_type = mime_type

class TranslationResponse:
    def __init__(self, translated_texts: List[str], detected_source_language: str = None):
        self.translated_texts = translated_texts
        self.detected_source_language = detected_source_language
