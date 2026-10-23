from __future__ import annotations

from google.cloud import texttospeech

from speech_client import (
    build_voice_params,
    get_google_tts_client,
    get_google_tts_model_config,
)
from speech_models import AudioResult, SpeechSynthesisRequest


def synthesize_text(request: SpeechSynthesisRequest) -> AudioResult:
    client = get_google_tts_client()
    response = client.synthesize_speech(
        request=texttospeech.SynthesizeSpeechRequest(
            input=texttospeech.SynthesisInput(text=request.text),
            voice=texttospeech.VoiceSelectionParams(
                **build_voice_params(request.language_code, request.voice)
            ),
            audio_config=texttospeech.AudioConfig(
                speaking_rate=request.speaking_rate,
                pitch=request.pitch,
                **get_google_tts_model_config(
                    request.audio_encoding, request.sample_rate_hertz
                ),
            ),
        )
    )
    return AudioResult(
        audio_bytes=response.audio_content,
        audio_encoding=request.audio_encoding,
        provider="google-cloud-texttospeech",
        voice_name=request.voice,
        sample_rate_hertz=request.sample_rate_hertz,
    )
