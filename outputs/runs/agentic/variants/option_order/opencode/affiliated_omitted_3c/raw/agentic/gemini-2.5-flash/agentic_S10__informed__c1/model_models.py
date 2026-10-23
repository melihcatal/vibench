import json
from typing import List, Dict, Any, Optional


class LLMRequest:
    def __init__(
        self,
        prompt: str,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 150,
    ):
        self.prompt = prompt
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens


class LLMResponse:
    def __init__(self, text: str, finish_reason: Optional[str] = None):
        self.text = text
        self.finish_reason = finish_reason


class ModerationRequest:
    def __init__(self, text: str):
        self.text = text


class ModerationResponse:
    def __init__(self, flagged: bool, categories: Dict[str, Any]):
        self.flagged = flagged
        self.categories = categories


class TranslationRequest:
    def __init__(self, text: str, target_language: str = "en"):
        self.text = text
        self.target_language = target_language


class TranslationResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text


class EmbeddingRequest:
    def __init__(self, text: str, model: str = "text-embedding-ada-002"):
        self.text = text
        self.model = model


class EmbeddingResponse:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding


class TTSRequest:
    def __init__(self, text: str, voice_name: str = "en-US-JennyNeural"):
        self.text = text
        self.voice_name = voice_name


class TTSResponse:
    def __init__(self, audio_content: bytes):
        self.audio_content = audio_content
