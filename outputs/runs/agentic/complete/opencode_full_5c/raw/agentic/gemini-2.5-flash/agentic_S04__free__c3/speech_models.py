import dataclasses
from typing import List, Dict, Any, Optional

@dataclasses.dataclass
class TranscriptionConfig:
    audio_uri: str
    language_code: str = "en-US"
    enable_speaker_diarization: bool = False
    min_speaker_count: int = 1
    max_speaker_count: int = 6
    enable_word_time_offsets: bool = False

@dataclasses.dataclass
class TranscriptionSegment:
    start_time: float
    end_time: float
    text: str
    speaker_tag: Optional[int] = None
    word_timestamps: Optional[List[Dict[str, Any]]] = None

@dataclasses.dataclass
class TranscriptionResult:
    operation_id: str
    transcript_text: str
    segments: List[TranscriptionSegment]

@dataclasses.dataclass
class TranslationRequest:
    text_segments: List[str]
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclasses.dataclass
class ModerationRequest:
    text_content: str

@dataclasses.dataclass
class SummarizationRequest:
    text_content: str

@dataclasses.dataclass
class EmbeddingRequest:
    text_segments: List[str}