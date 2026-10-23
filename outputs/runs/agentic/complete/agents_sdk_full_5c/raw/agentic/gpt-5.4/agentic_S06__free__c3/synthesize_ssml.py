from __future__ import annotations

from speech_client import GoogleSpeechClient, build_audio_config, build_voice_params
from speech_models import AudioResult, SynthesisRequest, coalesce_text_input, decode_base64_audio


def synthesize_ssml(request: SynthesisRequest) -> AudioResult:
    client = GoogleSpeechClient()
    payload = {
        "input": coalesce_text_input(ssml=request.ssml),
        "voice": build_voice_params(request.language_code, request.voice_name, request.gender),
        "audioConfig": build_audio_config(
            audio_encoding=request.audio_encoding,
            speaking_rate=request.speaking_rate,
            pitch=request.pitch,
            sample_rate_hertz=request.sample_rate_hertz,
        ),
    }
    data = client.post("/text:synthesize", payload)
    return AudioResult(
        provider="google-cloud-text-to-speech",
        audio_bytes=decode_base64_audio(data["audioContent"]),
        voice_name=request.voice_name,
    )
