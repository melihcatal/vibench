import os
import json
from google.cloud import speech
from google.cloud.speech_v1p1beta1 import enums

class SynthesisInput(TypedDict):
    text: str
    ssml: str

class SynthesisOutput(TypedDict):
    audio_content: bytes
    encoding: str


class VoiceSelectionParams(TypedDict):
    name: str
    language_codes: List[str]


class AudioConfig(TypedDict):
    audio_encoding: str
    speaking_rate: float
    pitch: float
    prosody_strength: str


class ClientConfig(TypedDict):
    language_code: str
    sample_rate_hertz: int
    encoding: enums.RecognitionConfig.AudioEncoding
