from __future__ import annotations

import os

from elevenlabs import ElevenLabs

from translation_models import AudioPreviewResult


ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_TTS_MODEL", "eleven_multilingual_v2")
DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")


def generate_localized_audio_preview(text: str, voice_id: str | None = None) -> AudioPreviewResult:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        voice_id=voice_id or DEFAULT_VOICE_ID,
        model_id=ELEVENLABS_MODEL_ID,
        text=text,
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio)
    return AudioPreviewResult(
        audio=audio_bytes,
        content_type="audio/mpeg",
        provider="ElevenLabs",
        voice=voice_id or DEFAULT_VOICE_ID,
        raw={"model_id": ELEVENLABS_MODEL_ID},
    )
