from google.cloud.texttospeech_v1 import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    SsmlVoiceGender,
)
from typing import Optional


def create_text_input(text: str) -> SynthesisInput:
    return SynthesisInput(text=text)


def create_ssml_input(ssml: str) -> SynthesisInput:
    return SynthesisInput(ssml=ssml)


def create_voice(
    name: Optional[str],
    language_code: str,
    ssml_gender: Optional[SsmlVoiceGender] = None,
) -> VoiceSelectionParams:
    voice = VoiceSelectionParams(language_code=language_code)
    if name:
        voice.name = name
    if ssml_gender:
        voice.ssml_gender = ssml_gender
    return voice


def create_audio_config(
    speaking_rate: float = 1.0,
) -> AudioConfig:
    return AudioConfig(
        audio_encoding=AudioConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        speaking_rate=speaking_rate,
    )
