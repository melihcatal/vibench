import os
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings
from typing import Optional


def retrieval_audio_brief(brief_text: str) -> bytes:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.generate(
        text=brief_text,
        voice="Rachel",
        model="eleven_monolingual_v1",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True,
        ),
    )
    return audio
