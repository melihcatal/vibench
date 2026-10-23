import os
from typing import Optional
from elevenlabs import generate, play, set_api_key
from pydantic import BaseModel


class SpokenBriefRequest(BaseModel):
    text: str
    voice: str = "Rachel"
    model: str = "eleven_multilingual_v2"


class SpokenBriefResponse(BaseModel):
    audio: bytes
    voice: str
    model: str


def generate_spoken_brief(
    text: str,
    voice: str = "Rachel",
    model: str = "eleven_multilingual_v2"
) -> SpokenBriefResponse:
    """
    Generate a spoken brief from the model output using ElevenLabs TTS.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")
    
    set_api_key(api_key)
    audio = generate(
        text=text,
        voice=voice,
        model=model
    )
    
    return SpokenBriefResponse(
        audio=audio,
        voice=voice,
        model=model
    )