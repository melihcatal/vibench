from enum import Enum


class AudioEncoding(Enum):
    LINEAR16 = "LINEAR16"
    MP3 = "MP3"
    OGG_OPUS = "OGG_OPUS"


class VoiceGender(Enum):
    UNSPECIFIED = "SSML_VOICE_GENDER_UNSPECIFIED"
    MALE = "MALE"
    FEMALE = "FEMALE"
    NEUTRAL = "NEUTRAL"
