from __future__ import annotations

import os

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs


def generate_reviewer_brief_audio(
    brief_text: str,
    voice_id: str = "JBFqnCBsd6RMkjVDRZzb",
    model_id: str = "eleven_multilingual_v2",
) -> bytes:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=brief_text,
        output_format="mp3_44100_128",
        voice_settings=VoiceSettings(
            stability=0.4, similarity_boost=0.8, style=0.2, use_speaker_boost=True
        ),
    )
    return b"".join(audio)
