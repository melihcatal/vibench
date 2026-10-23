from dataclasses import dataclass
from google.cloud.texttospeech_v1.types import AudioEncoding


@dataclass
class VoiceSelectionParams:
    language_code: str
    name: str


@dataclass
class SynthesisInput:
    text: str = None
    ssml: str = None


@dataclass
class AudioConfig:
    audio_encoding: AudioEncoding
    speaking_rate: float = 1.0
    pitch: float = 0.0


@dataclass
class SynthesisResponse:
    audio_content: bytes
