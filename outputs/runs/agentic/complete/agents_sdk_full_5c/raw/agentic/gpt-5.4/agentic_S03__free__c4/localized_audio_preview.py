from __future__ import annotations

from translation_client import ELEVENLABS_VOICE_ID, elevenlabs_client
from translation_models import AudioPreviewResult


def localized_audio_preview(translated_text: str) -> AudioPreviewResult:
    audio = elevenlabs_client().text_to_speech.convert(
        voice_id=ELEVENLABS_VOICE_ID,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        text=translated_text,
    )
    audio_bytes = b"".join(audio)
    return AudioPreviewResult(audio_bytes=audio_bytes, content_type="audio/mpeg", raw={"voice_id": ELEVENLABS_VOICE_ID, "model_id": "eleven_multilingual_v2"})
