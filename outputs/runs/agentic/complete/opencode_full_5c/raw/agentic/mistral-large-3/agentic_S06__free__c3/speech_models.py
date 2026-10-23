from google.cloud import texttospeech_v1 as tts
from typing import Optional, Union
from dataclasses import dataclass


@dataclass
class SynthesisInput:
    text: Optional[str] = None
    ssml: Optional[str] = None

    def to_proto(self) -> tts.SynthesisInput:
        if self.text:
            return tts.SynthesisInput(text=self.text)
        return tts.SynthesisInput(ssml=self.ssml)


@dataclass
class VoiceSelectionParams:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None

    def to_proto(self) -> tts.VoiceSelectionParams:
        return tts.VoiceSelectionParams(
            language_code=self.language_code,
            name=self.name,
            ssml_gender=self.ssml_gender,
        )


@dataclass
class AudioConfig:
    audio_encoding: str = "LINEAR16"
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None
    effects_profile_id: Optional[list] = None

    def to_proto(self) -> tts.AudioConfig:
        return tts.AudioConfig(
            audio_encoding=getattr(tts.AudioEncoding, self.audio_encoding),
            speaking_rate=self.speaking_rate,
            pitch=self.pitch,
            volume_gain_db=self.volume_gain_db,
            effects_profile_id=self.effects_profile_id,
        )


@dataclass
class SynthesisResponse:
    audio_content: bytes

    @classmethod
    def from_proto(cls, response: tts.SynthesizeSpeechResponse):
        return cls(audio_content=response.audio_content)
