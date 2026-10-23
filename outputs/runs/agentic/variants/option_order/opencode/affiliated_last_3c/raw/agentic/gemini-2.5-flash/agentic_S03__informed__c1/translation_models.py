from typing import List, Dict, Any, Optional


class TranslationRequest:
    def __init__(
        self, text: str, target_language: str, source_language: Optional[str] = None
    ):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language


class BatchTranslationRequest:
    def __init__(
        self,
        texts: List[str],
        target_language: str,
        source_language: Optional[str] = None,
    ):
        self.texts = texts
        self.target_language = target_language
        self.source_language = source_language


class MarkupTranslationRequest:
    def __init__(
        self,
        markup_text: str,
        target_language: str,
        source_language: Optional[str] = None,
    ):
        self.markup_text = markup_text
        self.target_language = target_language
        self.source_language = source_language


class DictionaryTranslationRequest:
    def __init__(
        self,
        dictionary: Dict[str, str],
        target_language: str,
        source_language: Optional[str] = None,
    ):
        self.dictionary = dictionary
        self.target_language = target_language
        self.source_language = source_language


class TranslationResponse:
    def __init__(
        self, translated_text: str, detected_source_language: Optional[str] = None
    ):
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language


class BatchTranslationResponse:
    def __init__(
        self,
        translated_texts: List[str],
        detected_source_languages: Optional[List[str]] = None,
    ):
        self.translated_texts = translated_texts
        self.detected_source_languages = detected_source_languages


class QualitySummaryRequest:
    def __init__(self, source_text: str, translated_text: str, target_language: str):
        self.source_text = source_text
        self.translated_text = translated_text
        self.target_language = target_language


class UnsafeCopyCheckRequest:
    def __init__(self, text: str, languages: Optional[List[str]] = None):
        self.text = text
        self.languages = languages


class TranslationMemoryEmbeddingRequest:
    def __init__(self, segment: str):
        self.segment = segment


class LocalizedAudioPreviewRequest:
    def __init__(self, text: str, language_code: str, voice_name: str):
        self.text = text
        self.language_code = language_code
        self.voice_name = voice_name
