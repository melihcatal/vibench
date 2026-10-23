from __future__ import annotations

import os

from elevenlabs import ElevenLabs

from model_models import SpeechResult

DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
DEFAULT_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")


def generate_spoken_brief(text: str, voice_id: str = DEFAULT_VOICE_ID) -> SpeechResult:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY is required")

    client = ElevenLabs(api_key=api_key)
    audio_iter = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=DEFAULT_MODEL_ID,
        output_format="mp3_44100_128",
        text=text,
    )
    audio_bytes = b"".join(audio_iter)
    return SpeechResult(
        provider="elevenlabs",
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        voice=voice_id,
    )
