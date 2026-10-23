from typing import List, Dict, Any, Literal, Optional
from dataclasses import dataclass

@dataclass
class TranscriptionConfig:
    region: str
    api_key: str
    job_name: Optional[str] = None

@dataclass
class TranscriptionPayload:
    audio_uri: str
    language_code: str
    diarization_enabled: bool = False
    word_level_timestamps_enabled: bool = False

@dataclass
class TranscriptionJob:
    job_id: str
    status: Literal['NOT_STARTED', 'RUNNING', 'SUCCEEDED', 'FAILED', 'SUBMITTED']
    results: Optional[Dict[str, Any]] = None

@dataclass
class TranscriptSegment:
    start_time: str
    end_time: str
    text: str
    speaker: Optional[int] = None
    words: Optional[List[Dict[str, Any]]] = None

@dataclass
class DiarizationResult:
    segments: List[TranscriptSegment]

@dataclass
class TimestampResult:
    segments: List[TranscriptSegment]
