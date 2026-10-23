from dataclasses import dataclass
from typing import Optional, List, Union
from google.cloud.texttospeech_v1.types import (
    Voice,
    SynthesisInput,
    AudioConfig,
    VoiceSelectionParams,
    SynthesizeSpeechResponse,
)


@dataclass
class TTSRequest:
    text: str
    ssml: Optional[str] = None
    language_code: Optional[str] = None
    voice_name: Optional[str] = None
    audio_encoding: str = "MP3"
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None


@dataclass
class TTSResponse:
    audio_content: bytes
    audio_encoding: str


@dataclass
class VoiceInfo:
    name: str
    language_codes: List[str]
    ssml_gender: str
    natural_sample_rate_hertz: int


def normalize_request(request: TTSRequest) -> dict:
    input_data = SynthesisInput()
    if request.ssml:
        input_data.ssml = request.ssml
    else:
        input_data.text = request.text

    voice_params = VoiceSelectionParams(
        language_code=request.language_code, name=request.voice_name
    )

    audio_config = AudioConfig(
        audio_encoding=request.audio_encoding,
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
    )

    return {"input": input_data, "voice": voice_params, "audio_config": audio_config}


def normalize_response(response: SynthesizeSpeechResponse) -> TTSResponse:
    return TTSResponse(audio_content=response.audio_content, audio_encoding="MP3")


def normalize_voice_list(voices: List[Voice]) -> List[VoiceInfo]:
    return [
        VoiceInfo(
            name=voice.name,
            language_codes=voice.language_codes,
            ssml_gender=voice.ssml_gender.name,
            natural_sample_rate_hertz=voice.natural_sample_rate_hertz,
        )
        for voice in voices
    ]
