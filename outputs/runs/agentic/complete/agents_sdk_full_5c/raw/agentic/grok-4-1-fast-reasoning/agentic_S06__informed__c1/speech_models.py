from google.cloud.texttospeech import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    AudioEncoding
)

def make_text_input(text: str) -> SynthesisInput:
    return SynthesisInput(text=text)

def make_ssml_input(ssml: str) -> SynthesisInput:
    return SynthesisInput(ssml=ssml)

def make_voice_params(language_code: str, name: str = None) -> VoiceSelectionParams:
    return VoiceSelectionParams(language_code=language_code, name=name)

def make_audio_config(encoding: AudioEncoding = AudioEncoding.MP3) -> AudioConfig:
    return AudioConfig(audio_encoding=encoding)