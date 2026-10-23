from pydantic import BaseModel
from typing import Optional, List


class TranscriptionRequest(BaseModel):
    audio_url: str
    speaker_labels: bool = False
    language_code: str = "en"
    word_timestamps: bool = True


class SpeakerLabel(BaseModel):
    speaker: str
    text: str
    start: int
    end: int


class WordTimestamp(BaseModel):
    word: str
    start: int
    end: int