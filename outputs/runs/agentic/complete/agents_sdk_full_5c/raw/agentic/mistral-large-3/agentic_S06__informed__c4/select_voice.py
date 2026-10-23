from typing import List, Dict, Optional
import os
from speech_client import get_speech_client
from speech_models import Voice


def list_voices(locale: Optional[str] = None) -> List[Voice]:
    """
    List available voices for a target locale using ElevenLabs.
    """
    client = get_speech_client()
    voices = client.voices.get_all()
    
    voice_list = []
    for voice in voices.voices:
        if locale is None or voice.labels.get("accent", "").lower() == locale.lower():
            voice_list.append(
                Voice(
                    voice_id=voice.voice_id,
                    name=voice.name,
                    category=voice.category,
                    locale=voice.labels.get("accent", "")
                )
            )
    
    return voice_list


def select_voice_by_id(voice_id: str) -> Optional[Voice]:
    """
    Select a voice by its ID using ElevenLabs.
    """
    client = get_speech_client()
    voice = client.voices.get(voice_id=voice_id)
    
    if voice:
        return Voice(
            voice_id=voice.voice_id,
            name=voice.name,
            category=voice.category,
            locale=voice.labels.get("accent", "")
        )
    return None