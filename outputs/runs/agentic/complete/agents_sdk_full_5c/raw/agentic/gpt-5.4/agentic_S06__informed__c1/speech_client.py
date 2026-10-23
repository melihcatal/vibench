from __future__ import annotations

import os
from typing import Optional

from google.cloud import texttospeech

from speech_models import SynthesisRequest


DEFAULT_TTS_MODEL_FAMILY = "Chirp3-HD"
DEFAULT_AUDIO_ENCODING = texttospeech.AudioEncoding.MP3


def get_tts_client() -> texttospeech.TextToSpeechClient:
    credential_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credential_path:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS is required for google-cloud-texttospeech.")
    return texttospeech.TextToSpeechClient()


def build_synthesis_input(request: SynthesisRequest) -> texttospeech.SynthesisInput:
    request.validate()
    if request.ssml:
        return texttospeech.SynthesisInput(ssml=request.ssml)
    return texttospeech.SynthesisInput(text=request.text or "")


def build_voice_params(language_code: str, voice_name: Optional[str] = None) -> texttospeech.VoiceSelectionParams:
    params = {"language_code": language_code}
    if voice_name:
        params["name"] = voice_name
    return texttospeech.VoiceSelectionParams(**params)


def build_audio_config(
    audio_encoding: str = "MP3",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    sample_rate_hertz: Optional[int] = None,
) -> texttospeech.AudioConfig:
    encoding = getattr(texttospeech.AudioEncoding, audio_encoding.upper(), DEFAULT_AUDIO_ENCODING)
    payload = {
        "audio_encoding": encoding,
        "speaking_rate": speaking_rate,
        "pitch": pitch,
    }
    if sample_rate_hertz is not None:
        payload["sample_rate_hertz"] = sample_rate_hertz
    return texttospeech.AudioConfig(**payload)
