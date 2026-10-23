from __future__ import annotations

from google.cloud import texttospeech

from speech_client import GoogleTTSClientFactory
from speech_models import AudioResult, SSMLRequest


PROVIDER = "google-cloud-texttospeech"


def synthesize_ssml(request: SSMLRequest) -> AudioResult:
    client = GoogleTTSClientFactory.create_client()
    input_ssml = texttospeech.SynthesisInput(ssml=request.normalized_ssml())
    voice = GoogleTTSClientFactory.voice_params(request.voice, request.language_code)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=GoogleTTSClientFactory.audio_encoding_for(request.audio_encoding),
        sample_rate_hertz=request.sample_rate_hz,
    )
    response = client.synthesize_speech(input=input_ssml, voice=voice, audio_config=audio_config)
    return AudioResult(
        audio_bytes=response.audio_content,
        audio_encoding=request.audio_encoding,
        provider=PROVIDER,
        voice=voice.name,
        sample_rate_hz=request.sample_rate_hz,
        extra={"input_type": "ssml", "model_name": getattr(voice, "model_name", None)},
    )
