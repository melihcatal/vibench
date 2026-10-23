from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class TranscriptionRequest(BaseModel):
    audio_url: str
    speaker_labels: bool = False
    word_timestamps: bool = False


class Word(BaseModel):
    text: str
    start: int
    end: int
    confidence: float


class Utterance(BaseModel):
    speaker: Optional[str]
    text: str
    start: int
    end: int
    words: List[Word]


class TranscriptionResponse(BaseModel):
    id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[Word]] = None
    utterances: Optional[List[Utterance]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status,
            "text": self.text,
            "words": [word.dict() for word in self.words] if self.words else None,
            "utterances": [utterance.dict() for utterance in self.utterances]
            if self.utterances
            else None,
        }
