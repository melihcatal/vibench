from typing import Dict, Any, List, Optional

from pydantic import BaseModel, Field


class TranscriptionSubmitRequest(BaseModel):
    audio_url: str = Field(..., description="URL of the audio file to transcribe")
    extra_params: Dict[str, Any] = Field(
        {}, description="Additional parameters for the transcription API"
    )


class TranscriptionResponse(BaseModel):
    id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[Dict[str, Any]]] = None
    utterances: Optional[List[Dict[str, Any]]] = None


class DiarizedTranscriptionRequest(TranscriptionSubmitRequest):
    pass


class TimestampedTranscriptionRequest(TranscriptionSubmitRequest):
    pass
