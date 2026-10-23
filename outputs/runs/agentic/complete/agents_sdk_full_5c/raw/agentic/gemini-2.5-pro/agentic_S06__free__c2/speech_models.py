from typing import List
from pydantic import BaseModel, Field


class VoiceDetail(BaseModel):
    """Represents details of a specific synthesis voice."""
    name: str
    language_codes: List[str]
    ssml_gender: str


class SynthesisRequest(BaseModel):
    """Represents a request for speech synthesis."""
    text: str = Field(description="The plain text to synthesize.")
    voice_name: str = Field(default="en-US-Wavenet-D", description="The name of the voice to use.")
    language_code: str = Field(default="en-US", description="The language code of the voice.")
