from typing import Optional
from google.cloud.texttospeech_v1 import (
    VoiceSelectionParams,
    AudioConfig,
    AudioEncoding,
)


def make_voice_params(
    language_code: str = "en-US", name: Optional[str] = None
) -> VoiceSelectionParams:
    return VoiceSelectionParams(
        language_code=language_code,
        name=name or f"{language_code}-Wavenet-D",
    )


def make_audio_config(
    encoding: AudioEncoding = AudioEncoding.MP3,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
) -> AudioConfig:
    return AudioConfig(
        audio_encoding=encoding,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )
