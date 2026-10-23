from typing import List, Optional
from pydantic import BaseModel
from typing import Any


class Word(BaseModel):
    word: str
    start: float  # seconds
    end: float  # seconds
    confidence: Optional[float] = None


class SpeakerUtterance(BaseModel):
    speaker: str
    text: str
    words: List[Word]
    start: float
    end: float


class Transcript(BaseModel):
    id: str
    text: str
    utterances: List[SpeakerUtterance]
    words: List[Word]
    status: str


def normalize_transcript(raw_transcript: Any) -> Transcript:
    utterances = []
    if hasattr(raw_transcript, "utterances"):
        for utt in raw_transcript.utterances:
            words = [
                Word(
                    word=w.word,
                    start=w.start / 1000.0,
                    end=w.end / 1000.0,
                    confidence=getattr(w, "confidence", None),
                )
                for w in utt.words
            ]
            utterances.append(
                SpeakerUtterance(
                    speaker=utt.speaker,
                    text=utt.text,
                    words=words,
                    start=utt.start / 1000.0,
                    end=utt.end / 1000.0,
                )
            )
    words = [
        Word(
            word=w.word,
            start=w.start / 1000.0,
            end=w.end / 1000.0,
            confidence=getattr(w, "confidence", None),
        )
        for w in raw_transcript.words
    ]
    return Transcript(
        id=raw_transcript.id,
        text=raw_transcript.text,
        utterances=utterances,
        words=words,
        status=str(raw_transcript.status),
    )
