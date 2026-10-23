# [HELPER] speech_models.py

from typing import TypedDict, Literal, Optional
from google.cloud import texttospeech_v1 as texttospeech


class SynthesizeInput(TypedDict):
    text: Optional[str] = None
    ssml: Optional[str] = None


class VoiceSelection(TypedDict):
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[
        Literal["SSML_VOICE_GENDER_UNSPECIFIED", "MALE", "FEMALE", "NEUTRAL"]
    ] = None


class AudioConfig(TypedDict):
    audio_encoding: Literal["MP3", "LINEAR16", "OGG_OPUS", "RAW_OPUS"]
    sample_rate_hertz: Optional[int] = None
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None


class SynthesisRequest(TypedDict):
    input: SynthesizeInput
    voice: VoiceSelection
    audio_config: AudioConfig


class SynthesisResponse(TypedDict):
    audio_content: bytes  # raw audio bytes
    # other fields omitted for brevity
