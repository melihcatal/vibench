from pydantic import BaseModel, Field
from typing import Optional, List


class SpeechRequest(BaseModel):
    text: Optional[str] = None
    ssml: Optional[str] = None


class VoiceSelection(BaseModel):
    language_code: str = Field(default="en-US")
    name: Optional[str] = None
    ssml_gender: Optional[str] = Field(default="NEUTRAL")


class AudioConfig(BaseModel):
    audio_encoding: str = Field(default="MP3")


class SynthesisRequest(BaseModel):
    input: SpeechRequest
    voice: VoiceSelection
    audio_config: AudioConfig


class Voice(BaseModel):
    language_codes: List[str]
    name: str
    ssml_gender: str
    natural_sample_rate_hertz: int


class VoicesResponse(BaseModel):
    voices: List[Voice]
