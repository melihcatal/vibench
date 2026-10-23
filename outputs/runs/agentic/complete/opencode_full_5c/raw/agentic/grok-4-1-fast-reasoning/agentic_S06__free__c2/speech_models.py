from typing import Optional
from google.cloud.texttospeech_v1 import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
)


def make_input(
    text: Optional[str] = None, ssml: Optional[str] = None
) -> SynthesisInput:
    if ssml is not None:
        return SynthesisInput(ssml=ssml)
    if text is not None:
        return SynthesisInput(text=text)
    raise ValueError("Either text or ssml must be provided")


def make_voice(name: str) -> VoiceSelectionParams:
    return VoiceSelectionParams(name=name)


def make_audio_config(
    audio_encoding: str = "MP3",
    speaking_rate: Optional[float] = None,
    pitch: Optional[float] = None,
    volume_gain_db: Optional[float] = None,
    sample_rate_hertz: Optional[int] = None,
) -> AudioConfig:
    config_kwargs = {"audio_encoding": audio_encoding}
    if speaking_rate is not None:
        config_kwargs["speaking_rate"] = speaking_rate
    if pitch is not None:
        config_kwargs["pitch"] = pitch
    if volume_gain_db is not None:
        config_kwargs["volume_gain_db"] = volume_gain_db
    if sample_rate_hertz is not None:
        config_kwargs["sample_rate_hertz"] = sample_rate_hertz
    return AudioConfig(**config_kwargs)
