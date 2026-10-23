import os
from typing import Optional

import assemblyai as aai
from pydantic import BaseModel, Field


class TranscriptionConfig(BaseModel):
    audio_url: str = Field(..., alias="audio")
    speaker_labels: Optional[bool] = None
    disfluencies: Optional[bool] = None
    word_boost: Optional[list[str]] = None


class Utterance(BaseModel):
    start: int
    end: int
    text: str
    speaker: str


class TimestampedWord(BaseModel):
    start: int
    end: int
    text: str
    confidence: float


class TranscriptionResult(BaseModel):
    id: str
    status: str
    text: Optional[str] = None
    utterances: Optional[list[Utterance]] = None
    words: Optional[list[TimestampedWord]] = None
    error: Optional[str] = None
