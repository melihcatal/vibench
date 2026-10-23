from pydantic import BaseModel, Field
from typing import List, Optional

class Word(BaseModel):
    word: str
    start: float
    end: float
    confidence: float
    punctuated_word: Optional[str] = None

class Alternative(BaseModel):
    transcript: str
    confidence: float
    words: List[Word]

class Channel(BaseModel):
    alternatives: List[Alternative]

class SpeechResponse(BaseModel):
    duration: float
    is_final: bool = Field(..., alias="is_final")
    speech_final: bool = Field(..., alias="speech_final")
    channel: Channel
    
    class Config:
        populate_by_name = True
