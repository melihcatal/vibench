from typing import Union, Optional
from google.cloud import texttospeech_v1 as texttospeech

class SynthesisInput:
    """
    Normalized input for text or SSML synthesis.
    """
    def __init__(
        self,
        text: Optional[str] = None,
        ssml: Optional[str] = None
    ):
        if text is None and ssml is None:
            raise ValueError("Either text or ssml must be provided.")
        self.text = text
        self.ssml = ssml
    
    def to_proto(self) -> texttospeech.SynthesisInput:
        return texttospeech.SynthesisInput(
            text=self.text,
            ssml=self.ssml
        )

class AudioConfig:
    """
    Normalized audio configuration for synthesis.
    """
    def __init__(
        self,
        audio_encoding: str = "MP3",
        speaking_rate: Optional[float] = None,
        pitch: Optional[float] = None,
        volume_gain_db: Optional[float] = None,
        sample_rate_hertz: Optional[int] = None,
        effects_profile_id: Optional[list] = None
    ):
        self.audio_encoding = audio_encoding
        self.speaking_rate = speaking_rate
        self.pitch = pitch
        self.volume_gain_db = volume_gain_db
        self.sample_rate_hertz = sample_rate_hertz
        self.effects_profile_id = effects_profile_id or []
    
    def to_proto(self) -> texttospeech.AudioConfig:
        return texttospeech.AudioConfig(
            audio_encoding=getattr(texttospeech.AudioEncoding, self.audio_encoding),
            speaking_rate=self.speaking_rate,
            pitch=self.pitch,
            volume_gain_db=self.volume_gain_db,
            sample_rate_hertz=self.sample_rate_hertz,
            effects_profile_id=self.effects_profile_id
        )