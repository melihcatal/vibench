from google.cloud import texttospeech
from enum import Enum


class AudioEncoding(Enum):
    LINEAR16 = "LINEAR16"
    MP3 = "MP3"
    OGG_OPUS = "OGG_OPUS"


class SynthesisInput:
    def __init__(self, text: str = None, ssml: str = None):
        if text and ssml:
            raise ValueError("Only one of 'text' or 'ssml' can be provided.")
        self.text = text
        self.ssml = ssml

    def to_google_cloud(self):
        if self.text:
            return texttospeech.SynthesisInput(text=self.text)
        elif self.ssml:
            return texttospeech.SynthesisInput(ssml=self.ssml)
        else:
            raise ValueError("Either 'text' or 'ssml' must be provided.")


class VoiceSelectionParams:
    def __init__(self, language_code: str, name: str = None, ssml_gender: str = None):
        self.language_code = language_code
        self.name = name
        self.ssml_gender = ssml_gender

    def to_google_cloud(self):
        return texttospeech.VoiceSelectionParams(
            language_code=self.language_code,
            name=self.name,
            ssml_gender=texttospeech.SsmlVoiceGender[self.ssml_gender]
            if self.ssml_gender
            else None,
        )


class AudioConfig:
    def __init__(
        self,
        audio_encoding: AudioEncoding,
        speaking_rate: float = None,
        pitch: float = None,
    ):
        self.audio_encoding = audio_encoding
        self.speaking_rate = speaking_rate
        self.pitch = pitch

    def to_google_cloud(self):
        return texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding[self.audio_encoding.value],
            speaking_rate=self.speaking_rate,
            pitch=self.pitch,
        )
