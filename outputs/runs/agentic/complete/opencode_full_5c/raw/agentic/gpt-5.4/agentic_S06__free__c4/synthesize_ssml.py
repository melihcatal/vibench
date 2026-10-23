from __future__ import annotations

from xml.sax.saxutils import escape

from speech_client import OPENAI_TTS_MODEL, get_openai_client, pick_voice_for_locale
from speech_models import AudioResult, TTSRequest


def _ssml_to_openai_prompt(request: TTSRequest) -> str:
    rate = request.speaking_rate if request.speaking_rate is not None else 1.0
    pitch = request.pitch if request.pitch is not None else 0.0
    return (
        "Render the following SSML-style narration faithfully. "
        f"Use speaking rate {rate} and pitch offset {pitch}. Content: {escape(request.text)}"
    )


def synthesize_ssml(request: TTSRequest) -> AudioResult:
    client = get_openai_client()
    voice = request.voice or pick_voice_for_locale(request.locale).voice_id
    payload = request.to_openai_speech_payload(model=OPENAI_TTS_MODEL, voice=voice)
    payload["input"] = _ssml_to_openai_prompt(request)
    response = client.audio.speech.create(**payload)
    audio_bytes = response.read()
    return AudioResult(
        provider="openai",
        model=OPENAI_TTS_MODEL,
        voice=voice,
        audio_bytes=audio_bytes,
        content_type=f"audio/{request.audio_format}",
        sample_rate_hz=request.sample_rate_hz,
    )
