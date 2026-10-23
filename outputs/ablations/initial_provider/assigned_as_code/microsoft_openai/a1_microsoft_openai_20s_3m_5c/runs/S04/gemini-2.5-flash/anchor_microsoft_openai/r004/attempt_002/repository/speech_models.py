from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class TranscriptionRequest:
    display_name: str
    locale: str
    content_urls: List[str]
    word_level_timestamps_enabled: bool = True
    diarization_enabled: bool = True

@dataclass
class TranscriptionResponse:
    job_id: str
    status: str
    locale: str
    created_date_time: str
    last_action_date_time: str
    display_name: str
    links: dict = field(default_factory=dict)
    properties: dict = field(default_factory=dict)

@dataclass
class TranscriptionFile:
    path: str
    kind: str
    created_date_time: str
    links: dict = field(default_factory=dict)

@dataclass
class TranscriptionResult:
    combined_recognized_phrases: List[dict] = field(default_factory=list)
    recognized_phrases: List[dict] = field(default_factory=list)
    duration_in_seconds: Optional[float] = None
    combined_text: Optional[str] = None
    segments: List[dict] = field(default_factory=list)
