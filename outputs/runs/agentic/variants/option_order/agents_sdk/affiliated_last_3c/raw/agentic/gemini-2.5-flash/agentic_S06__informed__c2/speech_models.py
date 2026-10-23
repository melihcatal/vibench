from google.cloud import texttospeech
from typing import Dict, Any, Optional

class VoiceSelection:
    """Defines parameters for voice selection."""
    def __init__(self, language_code: str, name: Optional[str] = None, ssml_gender: Optional[texttospeech.SsmlVoiceGender] = None):
        self.language_code = language_code
        self.name = name
        self.ssml_gender = ssml_gender

    def to_proto(self) -> texttospeech.VoiceSelectionParams:
        return texttospeech.VoiceSelectionParams(
            language_code=self.language_code,
            name=self.name,
            ssml_gender=self.ssml_gender
        )

class AudioConfig:
    """Defines parameters for audio output."""
    def __init__(self, audio_encoding: texttospeech.AudioEncoding, speaking_rate: Optional[float] = None, pitch: Optional[float] = None):
        self.audio_encoding = audio_encoding
        self.speaking_rate = speaking_rate
        self.pitch = pitch

    def to_proto(self) -> texttospeech.AudioConfig:
        return texttospeech.AudioConfig(
            audio_encoding=self.audio_encoding,
            speaking_rate=self.speaking_rate,
            pitch=self.pitch
        )

