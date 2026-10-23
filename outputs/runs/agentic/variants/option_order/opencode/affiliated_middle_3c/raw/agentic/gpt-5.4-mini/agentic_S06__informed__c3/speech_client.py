import os
from typing import List, Optional

from elevenlabs import Voice, VoiceSettings, client as elevenlabs_client


def get_api_key() -> Optional[str]:
    return os.getenv("ELEVENLABS_API_KEY")


def get_client() -> elevenlabs_client.ElevenLabs:
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")
    return elevenlabs_client.ElevenLabs(api_key=api_key)


def default_voice_settings() -> VoiceSettings:
    return VoiceSettings(
        stability=0.5, similarity_boost=0.75, style=0.0, use_speaker_boost=True
    )


def list_voices() -> List[Voice]:
    return list(get_client().voices.get_all().voices)
