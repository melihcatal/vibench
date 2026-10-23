from __future__ import annotations

from translation_client import get_elevenlabs_client
from translation_models import AudioPreviewResult


def generate_localized_audio_preview(text: str, voice_id: str = "JBFqnCBsd6RMkjVDRZzb") -> AudioPreviewResult:
    client = get_elevenlabs_client()
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        text=text,
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio)
    return AudioPreviewResult(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        provider="elevenlabs",
        voice_id=voice_id,
        raw={"model_id": "eleven_multilingual_v2", "bytes": len(audio_bytes)},
    )
