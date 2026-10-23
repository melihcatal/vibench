from __future__ import annotations

import os

from elevenlabs import ElevenLabs

from translation_models import AudioPreviewResult


def generate_localized_audio_preview(
    text: str, voice_id: str, model_id: str = "eleven_multilingual_v2"
) -> AudioPreviewResult:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=text,
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio)
    return AudioPreviewResult(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        voice_id=voice_id,
        raw={"model_id": model_id, "provider": "ElevenLabs"},
    )
