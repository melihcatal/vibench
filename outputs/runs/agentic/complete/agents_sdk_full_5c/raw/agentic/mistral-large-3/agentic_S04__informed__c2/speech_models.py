from pydantic import BaseModel
from typing import Optional, List

class TranscriptionRequest(BaseModel):
    audio_url: str
    speaker_labels: bool = False
    language_code: str = "en_us"
    auto_chapters: bool = False
    entity_detection: bool = False

    def dict(self, **kwargs):
        base_dict = super().dict(**kwargs)
        base_dict["speaker_labels"] = base_dict.pop("speaker_labels")
        return base_dict

class DiarizedSegment(BaseModel):
    speaker: str
    text: str
    start: int
    end: int

class TimestampedWord(BaseModel):
    word: str
    start: int
    end: int