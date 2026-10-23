from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class TranscriptionConfig:
    audio_url: str
    diarization_enabled: bool = False
    word_timestamps_enabled: bool = False

@dataclass
class TranscriptionJob:
    id: str
    status: str
    transcript: Optional[str] = None
    words: Optional[List[Dict[str, Any]]] = None
    utterances: Optional[List[Dict[str, Any]]] = None

@dataclass
class TranslationRequest:
    text: str
    target_lang: str

@dataclass
class ModerationRequest:
    text: str

@dataclass
class SummaryRequest:
    text: str

@dataclass
class EmbeddingRequest:
    text: str
