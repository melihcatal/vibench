# [HELPER] speech_models.py
# Define local request, response, and normalization helpers for Text-to-Speech

from typing import TypedDict, Literal
from google.cloud.texttospeech import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    AudioEncoding,
    SSMLVoiceGender,
)


class SynthRequest(TypedDict):
    text: str
    ssml: str
    voice_name: str
    language_code: str
    ssml_gender: Literal[
        SSMLVoiceGender.FEMALE, SSMLVoiceGender.MALE, SSMLVoiceGender.NEUTRAL
    ]
    audio_encoding: Literal[
        AudioEncoding.LINEAR16, AudioEncoding.MP3, AudioEncoding.OGG_OPUS
    ]
    sample_rate_hertz: int


class SynthResponse(TypedDict):
    audio_content: bytes
    encoding: AudioEncoding
    sample_rate_hertz: int
    duration_seconds: float


class NormalizedAudioConfig(TypedDict):
    audio_encoding: AudioEncoding
    sample_rate_hertz: int
    num_channels: int = 1
    enable_biasing: bool = False


# Helper to normalize a SynthRequest into Google client arguments
def normalize_request(
    req: SynthRequest,
) -> tuple[SynthesisInput, VoiceSelectionParams, AudioConfig]:
    if req["ssml"]:
        input_ = SynthesisInput(ssml=req["ssml"])
    else:
        input_ = SynthesisInput(text=req["text"])

    voice = VoiceSelectionParams(
        language_code=req["language_code"],
        name=req["voice_name"],
        ssml_gender=getattr(SSMLVoiceGender, req["ssml_gender"].upper()),
    )

    audio = AudioConfig(
        audio_encoding=req["audio_encoding"],
        sample_rate_hertz=req["sample_rate_hertz"],
    )
    return input_, voice, audio
