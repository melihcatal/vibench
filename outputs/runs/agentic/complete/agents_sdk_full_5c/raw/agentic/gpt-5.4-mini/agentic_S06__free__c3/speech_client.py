from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import texttospeech

from speech_models import SynthesisRequest, normalize_text, normalize_ssml


@dataclass(frozen=True)
class SpeechConfig:
    project_id: Optional[str] = None
    default_language_code: str = "en-US"
    default_voice_name: Optional[str] = None
    default_audio_encoding: str = "MP3"


@lru_cache(maxsize=1)
def load_config() -> SpeechConfig:
    return SpeechConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT"),
        default_language_code=os.getenv("TTS_DEFAULT_LANGUAGE_CODE", "en-US"),
        default_voice_name=os.getenv("TTS_DEFAULT_VOICE_NAME"),
        default_audio_encoding=os.getenv("TTS_DEFAULT_AUDIO_ENCODING", "MP3"),
    )


@lru_cache(maxsize=1)
def get_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()


def build_voice_params(language_code: str, voice_name: Optional[str] = None) -> texttospeech.VoiceSelectionParams:
    return texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )


def build_audio_config(encoding: str = "MP3", speaking_rate: float = 1.0, pitch: float = 0.0) -> texttospeech.AudioConfig:
    encoding_value = getattr(texttospeech.AudioEncoding, encoding.upper(), texttospeech.AudioEncoding.MP3)
    return texttospeech.AudioConfig(audio_encoding=encoding_value, speaking_rate=speaking_rate, pitch=pitch)


def synthesize(request: SynthesisRequest) -> bytes:
    client = get_client()
    config = load_config()
    language_code = request.language_code or config.default_language_code
    voice_name = request.voice_name or config.default_voice_name
    voice = build_voice_params(language_code, voice_name)
    audio_config = build_audio_config(request.audio_encoding or config.default_audio_encoding, request.speaking_rate, request.pitch)

    if request.ssml:
        input_text = texttospeech.SynthesisInput(ssml=normalize_ssml(request.text))
    else:
        input_text = texttospeech.SynthesisInput(text=normalize_text(request.text))

    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    return response.audio_content
