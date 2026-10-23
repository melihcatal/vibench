from typing import Any, Dict, List, Optional


class ModelRequest:
    def __init__(self, prompt: str, **kwargs):
        self.prompt = prompt
        self.kwargs = kwargs


class ModelResponse:
    def __init__(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        self.text = text
        self.metadata = metadata if metadata is not None else {}


class SafetyCheckRequest:
    def __init__(self, text: str):
        self.text = text


class SafetyCheckResponse:
    def __init__(self, is_safe: bool, details: Dict[str, Any]):
        self.is_safe = is_safe
        self.details = details


class TranslationRequest:
    def __init__(
        self, text: str, target_language: str, source_language: Optional[str] = None
    ):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language


class TranslationResponse:
    def __init__(
        self, translated_text: str, detected_source_language: Optional[str] = None
    ):
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language


class EmbeddingRequest:
    def __init__(self, text: List[str]):
        self.text = text


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings


class AudioBriefingRequest:
    def __init__(self, text: str, language_code: str, voice_name: str):
        self.text = text
        self.language_code = language_code
        self.voice_name = voice_name


class AudioBriefingResponse:
    def __init__(self, audio_content: bytes):
        self.audio_content = audio_content
