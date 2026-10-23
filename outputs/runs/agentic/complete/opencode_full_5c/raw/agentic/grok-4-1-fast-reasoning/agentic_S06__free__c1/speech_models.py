from google.cloud.texttospeech_v1.types import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    AudioEncoding,
    SsmlVoiceGender,
)


def create_text_input(text: str) -> SynthesisInput:
    return SynthesisInput(text=text)


def create_ssml_input(ssml: str) -> SynthesisInput:
    return SynthesisInput(ssml=ssml)


def create_voice_params(
    language_code: str, name: str = None, ssml_gender: str = None
) -> VoiceSelectionParams:
    params = VoiceSelectionParams(language_code=language_code)
    if name:
        params.name = name
    if ssml_gender:
        try:
            params.ssml_gender = SsmlVoiceGender[ssml_gender.upper()]
        except KeyError:
            pass
    return params


def create_audio_config(
    encoding: str = "MP3",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    volume_gain_db: float = 0.0,
) -> AudioConfig:
    audio_encoding = AudioEncoding[encoding.upper()]
    return AudioConfig(
        audio_encoding=audio_encoding,
        speaking_rate=speaking_rate,
        pitch=pitch,
        volume_gain_db=volume_gain_db,
    )
