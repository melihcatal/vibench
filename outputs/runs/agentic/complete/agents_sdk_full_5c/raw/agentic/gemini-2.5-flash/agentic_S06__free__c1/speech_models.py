from typing import Dict, Literal

# Define common structures for Text-to-Speech requests/responses for local helper consistency
# These mirror Google Cloud Text-to-Speech API parameters but allow for local manipulation.

class VoiceParams:
    """Defines parameters for voice selection."""
    def __init__(self, language_code: str, name: str = None, ssml_gender: Literal["MALE", "FEMALE", "NEUTRAL", "UNSPECIFIED"] = "UNSPECIFIED"):
        self.language_code = language_code
        self.name = name
        self.ssml_gender = ssml_gender

    def to_dict(self) -> Dict:
        return {
            "language_code": self.language_code,
            "name": self.name,
            "ssml_gender": self.ssml_gender,
        }

class AudioEncoding:
    """Defines supported audio encodings."""
    MP3 = "MP3"
    LINEAR16 = "LINEAR16"
    OGG_OPUS = "OGG_OPUS"

class AudioConfig:
    """Defines parameters for audio output."""
    def __init__(self, audio_encoding: Literal["MP3", "LINEAR16", "OGG_OPUS"] = AudioEncoding.MP3, sample_rate_hertz: int = 0):
        self.audio_encoding = audio_encoding
        self.sample_rate_hertz = sample_rate_hertz

    def to_dict(self) -> Dict:
        return {
            "audio_encoding": self.audio_encoding,
            "sample_rate_hertz": self.sample_rate_hertz,
        }
