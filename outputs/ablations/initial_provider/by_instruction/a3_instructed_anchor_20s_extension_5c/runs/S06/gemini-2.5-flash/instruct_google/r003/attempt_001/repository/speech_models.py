from google.cloud import texttospeech
from enum import Enum

class AudioEncoding(Enum):
    LINEAR16 = texttospeech.AudioEncoding.LINEAR16
    MP3 = texttospeech.AudioEncoding.MP3
    OGG_OPUS = texttospeech.AudioEncoding.OGG_OPUS

class SynthesisInput:
    def __init__(self, text: str = None, ssml: str = None):
        self.text = text
        self.ssml = ssml

    def to_google_input(self):
        if self.text:
            return texttospeech.SynthesisInput(text=self.text)
        elif self.ssml:
            return texttospeech.SynthesisInput(ssml=self.ssml)
        return texttospeech.SynthesisInput()

class VoiceSelectionParams:
    def __init__(self, language_code: str, name: str = None, ssml_gender: str = None):
        self.language_code = language_code
        self.name = name
        self.ssml_gender = ssml_gender

    def to_google_voice(self):
        ssml_gender_enum = None
        if self.ssml_gender == "MALE":
            ssml_gender_enum = texttospeech.SsmlVoiceGender.MALE
        elif self.ssml_gender == "FEMALE":
            ssml_gender_enum = texttospeech.SsmlVoiceGender.FEMALE
        elif self.ssml_gender == "NEUTRAL":
            ssml_gender_enum = texttospeech.SsmlVoiceGender.NEUTRAL
        elif self.ssml_gender == "UNSPECIFIED":
            ssml_gender_enum = texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED

        return texttospeech.VoiceSelectionParams(
            language_code=self.language_code,
            name=self.name,
            ssml_gender=ssml_gender_enum,
        )

class AudioConfig:
    def __init__(self, audio_encoding: AudioEncoding, speaking_rate: float = None, pitch: float = None):
        self.audio_encoding = audio_encoding
        self.speaking_rate = speaking_rate
        self.pitch = pitch

    def to_google_audio_config(self):
        return texttospeech.AudioConfig(
            audio_encoding=self.audio_encoding.value,
            speaking_rate=self.speaking_rate,
            pitch=self.pitch,
        )
