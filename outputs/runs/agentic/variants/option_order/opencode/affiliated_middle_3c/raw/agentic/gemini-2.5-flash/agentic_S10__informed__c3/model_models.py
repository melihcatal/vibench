import dataclasses
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class ChatMessage:
    role: str
    content: str


@dataclasses.dataclass
class GenerateContentRequest:
    contents: List[ChatMessage]
    model: str
    temperature: Optional[float] = None
    max_output_tokens: Optional[int] = None


@dataclasses.dataclass
class Part:
    text: str


@dataclasses.dataclass
class Candidate:
    content: Dict[str, Any]  # This will contain 'parts' and 'role'


@dataclasses.dataclass
class GenerateContentResponse:
    candidates: List[Candidate]


@dataclasses.dataclass
class EmbeddingRequest:
    model: str
    text: str


@dataclasses.dataclass
class EmbeddingResponse:
    embedding: Dict[str, Any]


@dataclasses.dataclass
class ModerationRequest:
    input: str


@dataclasses.dataclass
class ModerationResponse:
    categories_analysis: List[Dict[str, Any]]
    harm_blockages: List[Dict[str, Any]]


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str


@dataclasses.dataclass
class TextToSpeechRequest:
    text: str
    language_code: str
    voice_name: str
    audio_encoding: str


@dataclasses.dataclass
class TextToSpeechResponse:
    audio_content: bytes
