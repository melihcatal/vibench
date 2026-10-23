from __future__ import annotations

from speech_client import OPENAI_TTS_MODEL, get_openai_client, pick_voice_for_locale
from speech_models import AudioResult, TTSRequest


def synthesize_text(request: TTSRequest) -> AudioResult:
    client = get_openai_client()
    voice = request.voice or pick_voice_for_locale(request.locale).voice_id
    response = client.audio.speech.create(
        **request.to_openai_speech_payload(model=OPENAI_TTS_MODEL, voice=voice)
    )
    audio_bytes = response.read()
    return AudioResult(
        provider="openai",
        model=OPENAI_TTS_MODEL,
        voice=voice,
        audio_bytes=audio_bytes,
        content_type=f"audio/{request.audio_format}",
        sample_rate_hz=request.sample_rate_hz,
    )
