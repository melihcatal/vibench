from typing import Optional
from google.cloud.texttospeech_v1beta1.types import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    SsmlVoiceGender,
)


def create_text_input(text: str) -> SynthesisInput:
    return SynthesisInput(text=text)


def create_ssml_input(ssml: str) -> SynthesisInput:
    return SynthesisInput(ssml=ssml)


def create_voice_params(
    language_code: str,
    name: Optional[str] = None,
    ssml_gender: Optional[SsmlVoiceGender] = None,
) -> VoiceSelectionParams:
    return VoiceSelectionParams(
        language_code=language_code,
        name=name,
        ssml_gender=ssml_gender,
    )


def create_audio_config(
    audio_encoding: str = "MP3",
    speaking_rate: Optional[float] = None,
    pitch: Optional[float] = None,
    volume_gain_db: Optional[float] = None,
) -> AudioConfig:
    config = {"audio_encoding": audio_encoding}
    if speaking_rate is not None:
        config["speaking_rate"] = speaking_rate
    if pitch is not None:
        config["pitch"] = pitch
    if volume_gain_db is not None:
        config["volume_gain_db"] = volume_gain_db
    return AudioConfig(**config)
