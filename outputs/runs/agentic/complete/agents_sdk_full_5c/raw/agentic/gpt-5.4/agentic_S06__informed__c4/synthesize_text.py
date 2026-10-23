from __future__ import annotations

from google.cloud import texttospeech

from speech_client import build_audio_config, build_voice_params, get_provider_name, get_tts_client
from speech_models import TTSRequest, TTSResult, ensure_text


def synthesize_text(request: TTSRequest) -> TTSResult:
    client = get_tts_client()
    synthesis_input = texttospeech.SynthesisInput(text=ensure_text(request.text, "text"))
    voice = build_voice_params(request.language_code, request.voice_name)
    audio_config = build_audio_config(
        audio_encoding=request.audio_encoding,
        sample_rate_hz=request.sample_rate_hz,
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    return TTSResult(
        audio_bytes=response.audio_content,
        audio_encoding=request.audio_encoding,
        voice_name=request.voice_name,
        language_code=request.language_code,
        provider=get_provider_name(),
        metadata={"google_api": "texttospeech.googleapis.com"},
    )
