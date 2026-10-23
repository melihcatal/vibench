from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class AudioEncoding(str, Enum):
    MP3 = "MP3"
    LINEAR16 = "LINEAR16"
    OGG_OPUS = "OGG_OPUS"


class VoiceGender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NEUTRAL = "NEUTRAL"


@dataclass
class SynthesisRequest:
    """Request model for text-to-speech synthesis."""

    text: str
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    voice_gender: VoiceGender = VoiceGender.NEUTRAL
    audio_encoding: AudioEncoding = AudioEncoding.MP3
    speaking_rate: float = 1.0
    pitch: float = 0.0
    ssml: bool = False

    def to_google_params(self):
        """Convert to Google Cloud TTS parameters."""
        from google.cloud import texttospeech

        gender_map = {
            VoiceGender.MALE: texttospeech.SsmlVoiceGender.MALE,
            VoiceGender.FEMALE: texttospeech.SsmlVoiceGender.FEMALE,
            VoiceGender.NEUTRAL: texttospeech.SsmlVoiceGender.NEUTRAL,
        }

        encoding_map = {
            AudioEncoding.MP3: texttospeech.AudioEncoding.MP3,
            AudioEncoding.LINEAR16: texttospeech.AudioEncoding.LINEAR16,
            AudioEncoding.OGG_OPUS: texttospeech.AudioEncoding.OGG_OPUS,
        }

        voice_params = texttospeech.VoiceSelectionParams(
            language_code=self.language_code, ssml_gender=gender_map[self.voice_gender]
        )

        if self.voice_name:
            voice_params.name = self.voice_name

        audio_config = texttospeech.AudioConfig(
            audio_encoding=encoding_map[self.audio_encoding],
            speaking_rate=self.speaking_rate,
            pitch=self.pitch,
        )

        if self.ssml:
            synthesis_input = texttospeech.SynthesisInput(ssml=self.text)
        else:
            synthesis_input = texttospeech.SynthesisInput(text=self.text)

        return synthesis_input, voice_params, audio_config


@dataclass
class SynthesisResponse:
    """Response model for text-to-speech synthesis."""

    audio_content: bytes
    request: SynthesisRequest
    audio_encoding: str
    sample_rate_hertz: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "audio_size_bytes": len(self.audio_content),
            "audio_encoding": self.audio_encoding,
            "sample_rate_hertz": self.sample_rate_hertz,
            "request": {
                "language_code": self.request.language_code,
                "voice_name": self.request.voice_name,
                "audio_encoding": self.request.audio_encoding.value,
            },
        }


def normalize_voice_name(voice_name: str) -> str:
    """Normalize voice name format."""
    if not voice_name:
        return ""

    voice_name = voice_name.strip()

    if "en-US" in voice_name and "Neural2" not in voice_name:
        return voice_name.replace("en-US-", "en-US-Neural2-")

    return voice_name


def parse_google_voice(voice_response) -> Dict[str, Any]:
    """Parse Google Cloud TTS voice response."""
    return {
        "name": voice_response.name,
        "language_codes": list(voice_response.language_codes),
        "gender": voice_response.ssml_gender.name,
        "natural_sample_rate_hertz": voice_response.natural_sample_rate_hertz,
    }
