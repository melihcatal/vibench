from typing import List, Dict, Any


class TranslationRequest:
    def __init__(
        self, text: str, target_language: str, source_language: str = ""
    ):  # source_language can be empty for auto-detection
        self.text = text
        self.target_language = target_language
        self.source_language = source_language


class BatchTranslationRequest:
    def __init__(
        self, texts: List[str], target_language: str, source_language: str = ""
    ):
        self.texts = texts
        self.target_language = target_language
        self.source_language = source_language


class DictionaryTranslationRequest:
    def __init__(
        self,
        dictionary: Dict[str, str],
        target_language: str,
        source_language: str = "",
    ):
        self.dictionary = dictionary
        self.target_language = target_language
        self.source_language = source_language


class TranslationResponse:
    def __init__(self, translated_text: str, detected_source_language: str = ""):
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language


class BatchTranslationResponse:
    def __init__(
        self, translated_texts: List[str], detected_source_languages: List[str] = None
    ):
        self.translated_texts = translated_texts
        self.detected_source_languages = (
            detected_source_languages if detected_source_languages is not None else []
        )


class DictionaryTranslationResponse:
    def __init__(self, translated_dictionary: Dict[str, str]):
        self.translated_dictionary = translated_dictionary


class QualitySummaryRequest:
    def __init__(
        self,
        original_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
    ):
        self.original_text = original_text
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language


class QualitySummaryResponse:
    def __init__(self, summary: str):
        self.summary = summary


class UnsafeContentCheckRequest:
    def __init__(self, text: str):
        self.text = text


class UnsafeContentCheckResponse:
    def __init__(self, is_unsafe: bool, categories: Dict[str, Any]):
        self.is_unsafe = is_unsafe
        self.categories = categories


class TranslationMemoryEmbeddingRequest:
    def __init__(self, segment: str, language: str):
        self.segment = segment
        self.language = language


class TranslationMemoryEmbeddingResponse:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding


class LocalizedAudioPreviewRequest:
    def __init__(
        self, text: str, language_code: str, voice_name: str = ""
    ):  # voice_name can be empty for default
        self.text = text
        self.language_code = language_code
        self.voice_name = voice_name


class LocalizedAudioPreviewResponse:
    def __init__(self, audio_content: bytes):
        self.audio_content = audio_content
