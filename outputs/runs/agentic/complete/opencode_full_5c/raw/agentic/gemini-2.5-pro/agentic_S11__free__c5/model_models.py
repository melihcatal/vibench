from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Iterator

import cohere
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from googleapiclient import discovery


@dataclass
class ModelRequest:
    prompt: str
    temperature: float = 0.75


@dataclass
class ModelResponse:
    text: str
    metadata: Dict[str, Any]


@dataclass
class StreamedResponse:
    response: cohere.responses.chat.StreamedChatResponse


@dataclass
class SafetyRating:
    is_safe: bool
    scores: Dict[str, float]


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: str


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]


@dataclass
class AudioResponse:
    audio_content: bytes
