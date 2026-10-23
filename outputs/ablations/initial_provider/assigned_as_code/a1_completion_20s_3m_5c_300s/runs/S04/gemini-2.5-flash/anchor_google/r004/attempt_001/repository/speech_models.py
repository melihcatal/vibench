import dataclasses
from typing import Optional, List

@dataclasses.dataclass
class TranscriptionResult:
    transcript: str
    word_timestamps: Optional[List[dict]] = None
    speaker_diarization: Optional[List[dict]] = None
