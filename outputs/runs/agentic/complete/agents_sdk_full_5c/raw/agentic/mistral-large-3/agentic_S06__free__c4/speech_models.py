from pydantic import BaseModel
from google.cloud import texttospeech_v1
from typing import Union


class SynthesisRequest(BaseModel):
    """Normalized request model for text-to-speech synthesis."""
    input: Union[texttospeech_v1.SynthesisInput, dict]
    voice: Union[texttospeech_v1.VoiceSelectionParams, dict]
    audio_config: Union[texttospeech_v1.AudioConfig, dict]

    class Config:
        arbitrary_types_allowed = True


class SynthesisResponse(BaseModel):
    """Normalized response model for synthesized audio."""
    audio_content: bytes