import dataclasses
from typing import Literal

@dataclasses.dataclass
class SynthesisInput:
    text: str
    voice_id: str = "alloy"  # Default voice for OpenAI TTS

@dataclasses.dataclass
class SynthesisSSMLInput:
    ssml: str
    voice_name: str
    locale: str

@dataclasses.dataclass
class Voice:
    id: str
    name: str
    locale: str
    gender: str
    description: str = ""

@dataclasses.dataclass
class SynthesisOutput:
    audio_content: bytes
    audio_format: str

@dataclasses.dataclass
class TranslationInput:
    text: str
    target_language: str

@dataclasses.dataclass
class TranslationOutput:
    translated_text: str

@dataclasses.dataclass
class SafetyCheckInput:
    text: str

@dataclasses.dataclass
class SafetyCheckOutput:
    is_safe: bool
    reasons: list[str]

@dataclasses.dataclass
class EmbeddingInput:
    text: str

@dataclasses.dataclass
class EmbeddingOutput:
    embedding: list[float]

@dataclasses.dataclass
class TranscriptionInput:
    audio_content: bytes
    audio_format: str
    language: str

@dataclasses.dataclass
class TranscriptionOutput:
    transcript: str
