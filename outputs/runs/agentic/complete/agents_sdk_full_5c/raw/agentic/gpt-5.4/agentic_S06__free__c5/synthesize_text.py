from __future__ import annotations

from google.cloud import texttospeech

from speech_client import build_audio_config, build_voice_params, get_texttospeech_client
from speech_models import SpeechSynthesisRequest, SynthesisResult


def synthesize_text(request: SpeechSynthesisRequest) -> SynthesisResult:
    if not request.text:
        raise ValueError("request.text is required for plain text synthesis")

    client = get_texttospeech_client()
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=request.text),
        voice=build_voice_params(request.language_code, request.voice_name),
        audio_config=build_audio_config(
            audio_encoding=request.audio_encoding,
            speaking_rate=request.speaking_rate,
            pitch=request.pitch,
            sample_rate_hertz=request.sample_rate_hz,
        ),
    )
    return SynthesisResult(
        audio_bytes=response.audio_content,
        audio_encoding=request.audio_encoding,
        voice_name=request.voice_name,
        sample_rate_hz=request.sample_rate_hz,
    )
