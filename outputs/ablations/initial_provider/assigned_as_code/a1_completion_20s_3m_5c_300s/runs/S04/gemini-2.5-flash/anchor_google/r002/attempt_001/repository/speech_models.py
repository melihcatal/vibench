from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class TranscriptionResult:
    job_id: str
    status: str
    transcript: str = None
    word_timestamps: List[Dict[str, Any]] = None
    speaker_tags: List[Dict[str, Any]] = None
