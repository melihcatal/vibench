from __future__ import annotations

import os

from elevenlabs import ElevenLabs

from model_models import SpokenBriefResult


DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")


def generate_spoken_brief(text: str, voice_id: str = DEFAULT_VOICE_ID) -> SpokenBriefResult:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        text=text,
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(chunk for chunk in audio)
    return SpokenBriefResult(provider="ElevenLabs", voice=voice_id, audio_bytes=audio_bytes, content_type="audio/mpeg")
