from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import base64
import json


@dataclass
class TTSRequest:
    text: str = ""
    voice: str = "alloy"
    model: str = "tts-1"
    response_format: str = "mp3"
    speed: float = 1.0
    input_type: str = "text"

    def to_openai_payload(self) -> dict:
        return {
            "model": self.model,
            "input": self.text,
            "voice": self.voice,
            "response_format": self.response_format,
            "speed": self.speed,
        }


@dataclass
class TTSResponse:
    audio_bytes: bytes = b""
    content_type: str = "audio/mpeg"
    model_used: str = ""
    voice_used: str = ""
    duration_estimate_sec: float = 0.0

    @property
    def audio_base64(self) -> str:
        return base64.b64encode(self.audio_bytes).decode("utf-8")

    def to_dict(self) -> dict:
        return {
            "content_type": self.content_type,
            "model_used": self.model_used,
            "voice_used": self.voice_used,
            "duration_estimate_sec": self.duration_estimate_sec,
            "audio_base64_preview": self.audio_base64[:64] + "...",
        }


@dataclass
class VoiceInfo:
    voice_id: str = ""
    name: str = ""
    locale: str = ""
    gender: str = ""
    styles: List[str] = field(default_factory=list)
    sample_rate_hz: int = 24000
    is_neural: bool = True

    def to_dict(self) -> dict:
        return {
            "voice_id": self.voice_id,
            "name": self.name,
            "locale": self.locale,
            "gender": self.gender,
            "styles": self.styles,
            "sample_rate_hz": self.sample_rate_hz,
            "is_neural": self.is_neural,
        }


@dataclass
class SSMLRequest:
    ssml: str = ""
    voice: str = "alloy"
    model: str = "tts-1"
    response_format: str = "mp3"
    speed: float = 1.0

    def to_openai_payload(self) -> dict:
        return {
            "model": self.model,
            "input": self.ssml,
            "voice": self.voice,
            "response_format": self.response_format,
            "speed": self.speed,
        }

    @staticmethod
    def build_ssml(
        text: str,
        voice_name: str = "alloy",
        pitch: str = "default",
        rate: str = "medium",
        volume: str = "default",
    ) -> str:
        ssml_parts = [
            '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis">',
            f'<voice name="{voice_name}">',
            f'<prosody pitch="{pitch}" rate="{rate}" volume="{volume}">',
            text,
            "</prosody>",
            "</voice>",
            "</speak>",
        ]
        return "".join(ssml_parts)


@dataclass
class TranslationRequest:
    text: str = ""
    source_lang: str = "auto"
    target_lang: str = "en"
    model: str = "gpt-4o"

    def to_openai_payload(self) -> dict:
        system_msg = {
            "role": "system",
            "content": f"You are a professional translator. Translate the following text from {self.source_lang} to {self.target_lang}. Return only the translated text.",
        }
        user_msg = {"role": "user", "content": self.text}
        return {
            "model": self.model,
            "messages": [system_msg, user_msg],
            "temperature": 0.0,
        }


@dataclass
class TranslationResponse:
    translated_text: str = ""
    source_lang_detected: str = ""
    target_lang: str = ""
    model_used: str = ""

    def to_dict(self) -> dict:
        return {
            "translated_text": self.translated_text,
            "source_lang_detected": self.source_lang_detected,
            "target_lang": self.target_lang,
            "model_used": self.model_used,
        }


@dataclass
class SafetyCheckRequest:
    text: str = ""

    def to_openai_payload(self) -> dict:
        return {"input": self.text}


@dataclass
class SafetyCheckResponse:
    is_safe: bool = True
    flagged: bool = False
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    model_used: str = ""

    def to_dict(self) -> dict:
        return {
            "is_safe": self.is_safe,
            "flagged": self.flagged,
            "categories": self.categories,
            "model_used": self.model_used,
        }


@dataclass
class EmbeddingRequest:
    text: str = ""
    model: str = "text-embedding-3-small"

    def to_openai_payload(self) -> dict:
        return {
            "model": self.model,
            "input": self.text,
        }


@dataclass
class EmbeddingResponse:
    embedding: List[float] = field(default_factory=list)
    model_used: str = ""
    dimensions: int = 0

    def to_dict(self) -> dict:
        return {
            "model_used": self.model_used,
            "dimensions": self.dimensions,
            "embedding_preview": self.embedding[:8] if self.embedding else [],
        }


@dataclass
class TranscriptRequest:
    audio_bytes: bytes = b""
    language: str = "en"
    model: str = "whisper-1"
    response_format: str = "json"

    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "language": self.language,
            "response_format": self.response_format,
        }


@dataclass
class TranscriptResponse:
    text: str = ""
    language_detected: str = ""
    duration_sec: float = 0.0
    model_used: str = ""
    words: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "language_detected": self.language_detected,
            "duration_sec": self.duration_sec,
            "model_used": self.model_used,
            "word_count": len(self.words),
        }


def normalize_voice_id(voice_id: str) -> str:
    known_voices = {
        "alloy": "alloy",
        "echo": "echo",
        "fable": "fable",
        "onyx": "onyx",
        "nova": "nova",
        "shimmer": "shimmer",
    }
    return known_voices.get(voice_id.lower().strip(), "alloy")


def estimate_duration_from_text(text: str, words_per_minute: float = 150.0) -> float:
    word_count = len(text.split())
    return (word_count / words_per_minute) * 60.0


def format_audio_bytes(audio_bytes: bytes, fmt: str = "mp3") -> bytes:
    return audio_bytes
