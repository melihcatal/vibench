"""
speech_models.py - Define local request, response, and normalization helpers for Text-to-Speech.

Provides Pydantic models for TTS synthesis requests, voice selection parameters,
SSML synthesis options, and audio output configuration. Includes normalization
helpers for payload construction and response parsing.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class AudioEncodingEnum(str, Enum):
    LINEAR16 = "LINEAR16"
    MP3 = "MP3"
    OGG_OPUS = "OGG_OPUS"
    MULAW = "MULAW"


class SSMLGenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NEUTRAL = "NEUTRAL"


class SynthesisRequest(BaseModel):
    """Request model for plain-text synthesis."""

    text: str = Field(..., min_length=1, max_length=5000, description="Plain text to synthesize")
    language_code: str = Field(..., description="BCP-47 language code, e.g. en-US, fr-FR")
    voice_name: Optional[str] = Field(None, description="Specific voice name, e.g. en-US-Wavenet-D")
    ssml_gender: Optional[SSMLGenderEnum] = Field(None, description="Preferred SSML voice gender")
    encoding: AudioEncodingEnum = Field(AudioEncodingEnum.MP3, description="Audio encoding format")
    speaking_rate: float = Field(1.0, ge=0.25, le=4.0, description="Speaking rate multiplier")
    pitch: float = Field(0.0, ge=-20.0, le=20.0, description="Pitch shift in semitones")
    volume_gain_db: float = Field(0.0, ge=-96.0, le=16.0, description="Volume gain in decibels")
    sample_rate_hertz: int = Field(24000, ge=8000, le=48000, description="Audio sample rate in Hz")

    @validator("text")
    def normalize_text(cls, v: str) -> str:
        return v.strip()

    def to_google_payload(self) -> Dict[str, Any]:
        """Convert to Google Cloud Text-to-Speech API request payload."""
        input_data: Dict[str, Any] = {"text": self.text}
        voice: Dict[str, Any] = {"languageCode": self.language_code}
        if self.voice_name:
            voice["name"] = self.voice_name
        if self.ssml_gender:
            voice["ssmlGender"] = self.ssml_gender.value
        audio_config: Dict[str, Any] = {
            "audioEncoding": self.encoding.value,
            "speakingRate": self.speaking_rate,
            "pitch": self.pitch,
            "volumeGainDb": self.volume_gain_db,
            "sampleRateHertz": self.sample_rate_hertz,
        }
        return {"input": input_data, "voice": voice, "audioConfig": audio_config}


class SSMLSynthesisRequest(BaseModel):
    """Request model for SSML-based synthesis."""

    ssml: str = Field(..., min_length=1, description="SSML markup string")
    language_code: str = Field(..., description="BCP-47 language code")
    voice_name: Optional[str] = Field(None, description="Specific voice name for SSML")
    ssml_gender: Optional[SSMLGenderEnum] = Field(None, description="Preferred voice. Required if voice_name not set")
    encoding: AudioEncodingEnum = Field(AudioEncodingEnum.MP3)
    speaking_rate: float = Field(1.0, ge=0.25, le=4.0)
    pitch: float = Field(0.0, ge=-20.0, le=20.0)
    volume_gain_db: float = Field(0.0, ge=-96.0, le=16.0)
    sample_rate_hertz: int = Field(24000, ge=8000, le=48000)

    @validator("ssml")
    def normalize_ssml(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped.startswith("<speak"):
            stripped = f"<speak>{stripped}</speak>"
        return stripped

    def to_google_payload(self) -> Dict[str, Any]:
        """Convert to Google Cloud Text-to-Speech API SSML request payload."""
        input_data: Dict[str, Any] = {"ssml": self.ssml}
        voice: Dict[str, Any] = {"languageCode": self.language_code}
        if self.voice_name:
            voice["name"] = self.voice_name
        if self.ssml_gender:
            voice["ssmlGender"] = self.ssml_gender.value
        audio_config: Dict[str, Any] = {
            "audioEncoding": self.encoding.value,
            "speakingRate": self.speaking_rate,
            "pitch": self.pitch,
            "volumeGainDb": self.volume_gain_db,
            "sampleRateHertz": self.sample_rate_hertz,
        }
        return {"input": input_data, "voice": voice, "audioConfig": audio_config}


class VoiceFilter(BaseModel):
    """Filter parameters for voice selection."""

    language_code: str = Field(..., description="BCP-47 language code")
    ssml_gender: Optional[SSMLGenderEnum] = Field(None)
    model: Optional[str] = Field(None, description="Voice model, e.g. standard, wavenet, neural2, studio")

    def to_google_filter(self) -> Dict[str, Any]:
        """Convert to Google Cloud voice list filter."""
        filters: Dict[str, Any] = {"languageCode": self.language_code}
        if self.ssml_gender:
            filters["ssmlGender"] = self.ssml_gender.value
        return filters


@dataclass
class VoiceInfo:
    """Normalized voice information."""

    name: str
    language_code: str
    ssml_gender: str
    natural_sample_rate_hertz: int
    supported_models: List[str] = field(default_factory=list)


@dataclass
class SynthesisResponse:
    """Normalized synthesis response containing audio data."""

    audio_content: bytes
    encoding: AudioEncodingEnum
    sample_rate_hertz: int
    audio_length_bytes: int

    @classmethod
    def from_google_response(cls, response: Any) -> "SynthesisResponse":
        """Parse Google Cloud Text-to-Speech response into normalized form."""
        audio_bytes = response.audio_content
        return cls(
            audio_content=audio_bytes,
            encoding=AudioEncodingEnum.MP3,
            sample_rate_hertz=24000,
            audio_length_bytes=len(audio_bytes),
        )


@dataclass
class VoiceListResponse:
    """Normalized voice list response."""

    voices: List[VoiceInfo]

    @classmethod
    def from_google_response(cls, response: Any) -> "VoiceListResponse":
        """Parse Google Cloud voice list response."""
        voices = []
        for v in response.voices:
            voices.append(
                VoiceInfo(
                    name=v.name,
                    language_code=v.language_codes[0] if v.language_codes else "",
                    ssml_gender=v.ssml_gender.name if v.ssml_gender else "NEUTRAL",
                    natural_sample_rate_hertz=v.natural_sample_rate_hertz,
                    supported_models=list(v.supported_model_types) if hasattr(v, "supported_model_types") else [],
                )
            )
        return cls(voices=voices)
