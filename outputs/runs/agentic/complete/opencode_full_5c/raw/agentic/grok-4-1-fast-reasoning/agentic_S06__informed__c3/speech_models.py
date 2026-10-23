from google.cloud import texttospeech
from typing import Optional


def build_text_input(text: str) -> texttospeech.SynthesisInput:
    return texttospeech.SynthesisInput(text=text)


def build_ssml_input(ssml: str) -> texttospeech.SynthesisInput:
    return texttospeech.SynthesisInput(ssml=ssml)


def build_voice(
    language_code: str,
    name: Optional[str] = None,
    ssml_gender: Optional[texttospeech.SsmlVoiceGender] = None,
) -> texttospeech.VoiceSelectionParams:
    params = texttospeech.VoiceSelectionParams(language_code=language_code)
    if name:
        params.name = name
    if ssml_gender:
        params.ssml_gender = ssml_gender
    return params


def build_audio_config(
    encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3,
) -> texttospeech.AudioConfig:
    return texttospeech.AudioConfig(audio_encoding=encoding)
