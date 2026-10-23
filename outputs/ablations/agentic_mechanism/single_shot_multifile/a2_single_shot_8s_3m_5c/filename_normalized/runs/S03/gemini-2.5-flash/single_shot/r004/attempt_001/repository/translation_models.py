from typing import List, Dict, Any

class TranslationRequest:
    def __init__(self, texts: List[str], target_language_code: str, source_language_code: str = None, mime_type: str = "text/plain"):
        self.texts = texts
        self.target_language_code = target_language_code
        self.source_language_code = source_language_code
        self.mime_type = mime_type

class TranslationResponse:
    def __init__(self, translations: List[str], detected_source_language_code: str = None):
        self.translations = translations
        self.detected_source_language_code = detected_source_language_code

class QualitySummaryRequest:
    def __init__(self, original_text: str, translated_text: str, source_language: str, target_language: str):
        self.original_text = original_text
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language

class SafetyCheckRequest:
    def __init__(self, text: str, language_code: str):
        self.text = text
        self.language_code = language_code

class SafetyCheckResponse:
    def __init__(self, is_unsafe: bool, reasons: List[str]):
        self.is_unsafe = is_unsafe
        self.reasons = reasons

class EmbeddingRequest:
    def __init__(self, text: str):
        self.text = text

class EmbeddingResponse:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding

class AudioPreviewRequest:
    def __init__(self, text: str, language_code: str, voice_name: str = "en-US-Wavenet-D"):
        self.text = text
        self.language_code = language_code
        self.voice_name = voice_name