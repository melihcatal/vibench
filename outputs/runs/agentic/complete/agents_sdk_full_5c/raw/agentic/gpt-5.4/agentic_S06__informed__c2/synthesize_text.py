from __future__ import annotations

from google.cloud import texttospeech

from speech_client import GoogleTTSClientFactory
from speech_models import AudioResult, TTSRequest


PROVIDER = "google-cloud-texttospeech"


def synthesize_text(request: TTSRequest) -> AudioResult:
    client = GoogleTTSClientFactory.create_client()
    input_text = texttospeech.SynthesisInput(text=request.normalized_text())
    voice = GoogleTTSClientFactory.voice_params(request.voice, request.language_code)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=GoogleTTSClientFactory.audio_encoding_for(request.audio_encoding),
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
        sample_rate_hertz=request.sample_rate_hz,
    )
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    return AudioResult(
        audio_bytes=response.audio_content,
        audio_encoding=request.audio_encoding,
        provider=PROVIDER,
        voice=voice.name,
        sample_rate_hz=request.sample_rate_hz,
        extra={"model_name": getattr(voice, "model_name", None)},
    )
