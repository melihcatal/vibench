from typing import Optional, List, Iterator
from pydantic import BaseModel


class SynthesisRequest(BaseModel):
    """
    Request model for text-to-speech synthesis.
    """
    text: str
    voice_id: str = "alloy"
    model: str = "tts-1"
    is_ssml: bool = False


class SynthesisResponse:
    """
    Response model for text-to-speech synthesis.
    """
    def __init__(self, audio_stream: Iterator[bytes]):
        self.audio_stream = audio_stream


class Voice(BaseModel):
    """
    Voice model for voice selection.
    """
    voice_id: str
    name: str
    category: str
    locale: str