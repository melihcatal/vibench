from typing import Dict, Any, List


class ModelRequest:
    def __init__(self, prompt: str, **kwargs):
        self.prompt = prompt
        self.params = kwargs


class ModelResponse:
    def __init__(self, text: str, metadata: Dict[str, Any]):
        self.text = text
        self.metadata = metadata


class SafetyCheckResult:
    def __init__(self, is_safe: bool, categories: Dict[str, Any]):
        self.is_safe = is_safe
        self.categories = categories


class TranslatedText:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language


class TextEmbedding:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding


class AudioBriefing:
    def __init__(self, audio_content: bytes, audio_format: str):
        self.audio_content = audio_content
        self.audio_format = audio_format
