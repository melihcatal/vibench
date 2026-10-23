from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class Word(BaseModel):
    text: str
    start: int
    end: int
    speaker: Optional[str] = None
    confidence: Optional[float] = None


class Utterance(BaseModel):
    text: str
    start: int
    end: int
    speaker: str
    words: List[Word]


class TranscriptionResult(BaseModel):
    id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[Word]] = None
    utterances: Optional[List[Utterance]] = None
    audio_url: Optional[str] = None
    error: Optional[str] = None

    @classmethod
    def from_assemblyai_transcript(
        cls, transcript: Dict[str, Any]
    ) -> "TranscriptionResult":
        words = None
        if "words" in transcript and transcript["words"]:
            words = [Word(**word) for word in transcript["words"]]

        utterances = None
        if "utterances" in transcript and transcript["utterances"]:
            utterances = [
                Utterance(**utterance) for utterance in transcript["utterances"]
            ]

        return cls(
            id=transcript["id"],
            status=transcript["status"],
            text=transcript.get("text"),
            words=words,
            utterances=utterances,
            audio_url=transcript.get("audio_url"),
            error=transcript.get("error"),
        )
