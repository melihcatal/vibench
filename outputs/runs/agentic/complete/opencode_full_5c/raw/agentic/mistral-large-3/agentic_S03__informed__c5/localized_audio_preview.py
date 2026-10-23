import os
from typing import List
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs


def localized_audio_preview(
    texts: List[str],
    voice_id: str = "pNInz6obpgDQGcFmaJgB",
) -> List[bytes]:
    """
    Generates spoken previews of translated copy using ElevenLabs Text to Speech.
    """
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio_previews = []

    for text in texts:
        audio = client.generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v2",
            voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.5),
        )
        audio_previews.append(audio)

    return audio_previews
