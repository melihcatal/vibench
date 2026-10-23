from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import os
from typing import Optional


def generate_localized_audio_preview(
    text: str,
    voice_id: Optional[str] = "21m00Tcm4TlvDq8ikWAM",
    model_id: str = "eleven_monolingual_v1",
) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    client = ElevenLabs(api_key=api_key)
    audio = client.generate(
        text=text,
        voice=voice_id,
        model=model_id,
        voice_settings=VoiceSettings(
            stability=0.5, similarity_boost=0.75, style=0.0, use_speaker_boost=True
        ),
    )
    return audio
