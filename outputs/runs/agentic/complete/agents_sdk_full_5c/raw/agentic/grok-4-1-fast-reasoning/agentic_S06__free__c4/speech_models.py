from google.cloud.texttospeech_v1.types import (
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
    name: str = None,
    ssml_gender: SsmlVoiceGender = SsmlVoiceGender.NEUTRAL
) -> VoiceSelectionParams:
    params = VoiceSelectionParams(language_code=language_code)
    if name:
        params.name = name
    params.ssml_gender = ssml_gender
    return params

def create_audio_config(
    audio_encoding: str,
    sample_rate_hertz: int = 24000,
    speaking_rate: float = 1.0
) -> AudioConfig:
    return AudioConfig(
        audio_encoding=audio_encoding,
        sample_rate_hertz=sample_rate_hertz,
        speaking_rate=speaking_rate,
    )
