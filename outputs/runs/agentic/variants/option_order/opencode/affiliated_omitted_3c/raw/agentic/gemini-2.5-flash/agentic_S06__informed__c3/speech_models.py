import io
from typing import Literal, Optional, List


class SynthesisRequest:
    def __init__(
        self, text: str, voice_id: str, model_id: str = "eleven_monolingual_v1"
    ):
        self.text = text
        self.voice_id = voice_id
        self.model_id = model_id


class SSMLSynthesisRequest:
    def __init__(
        self, ssml: str, voice_id: str, model_id: str = "eleven_monolingual_v1"
    ):
        self.ssml = ssml
        self.voice_id = voice_id
        self.model_id = model_id


class AudioResponse:
    def __init__(self, audio_bytes: io.BytesIO, content_type: str = "audio/mpeg"):
        self.audio_bytes = audio_bytes
        self.content_type = content_type


class Voice:
    def __init__(
        self, voice_id: str, name: str, category: str, description: Optional[str] = None
    ):
        self.voice_id = voice_id
        self.name = name
        self.category = category
        self.description = description


class TranslateRequest:
    def __init__(self, text: str, target_lang: str, source_lang: Optional[str] = None):
        self.text = text
        self.target_lang = target_lang
        self.source_lang = source_lang


class TranslateResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text


class ContentSafetyRequest:
    def __init__(self, text: str):
        self.text = text


class ContentSafetyResponse:
    def __init__(self, is_safe: bool, categories: Optional[dict] = None):
        self.is_safe = is_safe
        self.categories = categories


class EmbeddingRequest:
    def __init__(self, text: str, model: str = "text-embedding-ada-002"):
        self.text = text
        self.model = model


class EmbeddingResponse:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding


class TranscriptionRequest:
    def __init__(self, audio_file_path: str):
        self.audio_file_path = audio_file_path


class TranscriptionResponse:
    def __init__(self, transcript: str):
        self.transcript = transcript
