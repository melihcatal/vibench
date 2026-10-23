from __future__ import annotations

import os

from elevenlabs import ElevenLabs

from translation_models import AudioPreviewResult


DEFAULT_MODEL_ID = os.getenv("ELEVENLABS_TTS_MODEL", "eleven_multilingual_v2")
DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")


def localized_audio_preview(text: str, language_code: str = "en") -> AudioPreviewResult:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio_stream = client.text_to_speech.convert(
        voice_id=DEFAULT_VOICE_ID,
        model_id=DEFAULT_MODEL_ID,
        output_format="mp3_44100_128",
        text=text,
        voice_settings={"stability": 0.4, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True},
    )
    audio_bytes = b"".join(audio_stream)
    return AudioPreviewResult(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        provider="elevenlabs",
        voice_id=DEFAULT_VOICE_ID,
        raw={"language_code": language_code, "model_id": DEFAULT_MODEL_ID},
    )
