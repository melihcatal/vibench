from typing import Optional, Union
from google.cloud.texttospeech_v1.types import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    AudioEncoding,
    SsmlVoiceGender,
)

def build_synthesis_input(text: Optional[str] = None, ssml: Optional[str] = None) -> SynthesisInput:
    if ssml is not None:
        return SynthesisInput(ssml=ssml)
    if text is not None:
        return SynthesisInput(text=text)
    raise ValueError("Either text or ssml must be provided.")

def build_voice_params(
    language_code: str,
    name: Optional[str] = None,
    ssml_gender: Optional[SsmlVoiceGender] = None
) -> VoiceSelectionParams:
    params = VoiceSelectionParams(language_code=language_code)
    if name:
        params.name = name
    if ssml_gender:
        params.ssml_gender = ssml_gender
    return params

def build_audio_config(
    encoding: AudioEncoding = AudioEncoding.MP3,
    sample_rate_hertz: int = 24000
) -> AudioConfig:
    return AudioConfig(
        audio_encoding=encoding,
        sample_rate_hertz=sample_rate_hertz
    )
