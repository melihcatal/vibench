import os
from typing import List, Optional
from elevenlabs.client import ElevenLabs
from elevenlabs.types import Voice as ElevenLabsVoice
from speech_client import get_elevenlabs_client
from speech_models import Voice


def list_voices() -> List[Voice]:
    """
    Lists available voices from ElevenLabs.
    """
    client: ElevenLabs = get_elevenlabs_client()
    elevenlabs_voices: List[ElevenLabsVoice] = client.voices.get_all()

    voices = []
    for el_voice in elevenlabs_voices:
        voices.append(
            Voice(
                voice_id=el_voice.voice_id,
                name=el_voice.name,
                description=f"Category: {el_voice.category}"
                if el_voice.category
                else "No category",
            )
        )
    return voices


def select_voice_by_name(name: str) -> Optional[Voice]:
    """
    Selects a voice by its name from ElevenLabs.
    """
    voices = list_voices()
    for voice in voices:
        if voice.name.lower() == name.lower():
            return voice
    return None
