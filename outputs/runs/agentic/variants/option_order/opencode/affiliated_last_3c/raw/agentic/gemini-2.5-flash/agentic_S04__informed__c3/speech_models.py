import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class TranscriptionRequest:
    audio_uri: str
    language_code: str = "en-US"
    enable_speaker_diarization: bool = False
    enable_word_time_offsets: bool = False


@dataclasses.dataclass
class WordInfo:
    word: str
    start_time: float
    end_time: float
    speaker_tag: Optional[int] = None


@dataclasses.dataclass
class TranscriptionResult:
    transcript: str
    words: Optional[List[WordInfo]] = None
    speaker_diarization: Optional[List[str]] = None


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    parent: str = "projects/your-project-id/locations/global"  # Replace with your GCP Project ID and Location


@dataclasses.dataclass
class ModerationRequest:
    text: str


@dataclasses.dataclass
class SummarizationRequest:
    text: str


@dataclasses.dataclass
class EmbeddingRequest:
    text: str
