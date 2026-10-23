from dataclasses import dataclass
from enum import Enum

class AudioEncoding(Enum):
    UNSPECIFIED = 0
    LINEAR16 = 1 # Uncompressed 16-bit signed little-endian samples
    MP3 = 2
    OGG_OPUS = 3
    MULAW = 5

class SsmlGender(Enum):
    SSML_GENDER_UNSPECIFIED = 0
    MALE = 1
    FEMALE = 2
    NEUTRAL = 3

@dataclass
class SynthesisRequest:
    text_content: str = None
    ssml_content: str = None
    language_code: str = "en-US"
    voice_name: str = "en-US-Standard-C" # Example Google Cloud voice
    ssml_gender: SsmlGender = SsmlGender.FEMALE
    audio_encoding: AudioEncoding = AudioEncoding.MP3
