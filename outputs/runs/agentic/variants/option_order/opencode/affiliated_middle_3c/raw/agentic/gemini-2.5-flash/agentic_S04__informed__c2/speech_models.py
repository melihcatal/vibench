from typing import Optional, List
from pydantic import BaseModel


class TranscriptionRequest(BaseModel):
    audio_url: str
    speaker_diarization: Optional[bool] = False
    word_boost: Optional[List[str]] = None


class TranscriptionResult(BaseModel):
    id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[dict]] = None
    segments: Optional[List[dict]] = None
    utterances: Optional[List[dict]] = None
