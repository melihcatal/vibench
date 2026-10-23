from typing import List, Dict, Any, Optional

class TranslationRequest:
    def __init__(self, text: str, source_language: str, target_language: str, format: Optional[str] = None):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language
        self.format = format # 'html' or 'text'

class BatchTranslationRequest:
    def __init__(self, texts: List[str], source_language: str, target_language: str, format: Optional[str] = None):
        self.texts = texts
        self.source_language = source_language
        self.target_language = target_language
        self.format = format

class DictionaryTranslationRequest:
    def __init__(self, data: Dict[str, str], source_language: str, target_language: str):
        self.data = data
        self.source_language = source_language
        self.target_language = target_language

class TranslationResponse:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class BatchTranslationResponse:
    def __init__(self, texts: List[str], source_language: str, target_language: str):
        self.texts = texts
        self.source_language = source_language
        self.target_language = target_language

class DictionaryTranslationResponse:
    def __init__(self, data: Dict[str, str], source_language: str, target_language: str):
        self.data = data
        self.source_language = source_language
        self.target_language = target_language
