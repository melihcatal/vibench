from pydantic import BaseModel, Field
from typing import Optional


class VoiceSelectionParams(BaseModel):
    language_code: str = Field(..., example="en-US")
    name: Optional[str] = Field(None, example="en-US-Wavenet-D")
    ssml_gender: Optional[str] = Field(None, example="NEUTRAL")


class AudioConfig(BaseModel):
    audio_encoding: str = Field(..., example="MP3")
    speaking_rate: Optional[float] = Field(None, example=1.0)
    pitch: Optional[float] = Field(None, example=0.0)
