from enum import Enum
from typing import Dict, Any


class AudioOutputFormat(str, Enum):
    MP3 = "MP3"
    LINEAR16 = "LINEAR16"
    OGG_OPUS = "OGG_OPUS"


class VoiceSelectionParams:
    def __init__(self, language_code: str, name: str = None, ssml_gender: str = None):
        self.language_code = language_code
        self.name = name
        self.ssml_gender = ssml_gender


class SynthesisInput:
    def __init__(self, text: str = None, ssml: str = None):
        self.text = text
        self.ssml = ssml


class AudioConfig:
    def __init__(
        self,
        audio_encoding: AudioOutputFormat,
        speaking_rate: float = None,
        pitch: float = None,
    ):
        self.audio_encoding = audio_encoding
        self.speaking_rate = speaking_rate
        self.pitch = pitch
