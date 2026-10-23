from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class TranscriptionRequest(BaseModel):
    audio_url: str
    speaker_diarization: Optional[bool] = False
    word_timestamps: Optional[bool] = False


class TranscriptionResponse(BaseModel):
    id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[Dict[str, Any]]] = None
    utterances: Optional[List[Dict[str, Any]]] = None


class TranscriptionPollResponse(BaseModel):
    status: str
    text: Optional[str] = None
    words: Optional[List[Dict[str, Any]]] = None
    utterances: Optional[List[Dict[str, Any]]] = None
