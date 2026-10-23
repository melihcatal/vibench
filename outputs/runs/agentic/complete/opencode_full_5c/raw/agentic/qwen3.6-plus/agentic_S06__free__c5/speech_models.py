from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from enum import Enum


class AudioFormat(str, Enum):
    MP3 = "MP3"
    LINEAR16 = "LINEAR16"
    OGG_OPUS = "OGG_OPUS"
    MULAW = "MULAW"
    ALAW = "ALAW"


class VoiceGender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NEUTRAL = "NEUTRAL"


@dataclass
class TTSRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    ssml_gender: Optional[str] = None
    audio_encoding: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0
    effects_profile_id: Optional[str] = None

    def validate(self):
        if self.text is None and self.ssml is None:
            raise ValueError("Either 'text' or 'ssml' must be provided")
        if self.text is not None and self.ssml is not None:
            raise ValueError("Only one of 'text' or 'ssml' should be provided")
        if self.speaking_rate < 0.25 or self.speaking_rate > 4.0:
            raise ValueError("speaking_rate must be between 0.25 and 4.0")
        if self.pitch < -20.0 or self.pitch > 20.0:
            raise ValueError("pitch must be between -20.0 and 20.0")

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class TTSResponse:
    audio_content: bytes
    audio_format: str
    sample_rate_hertz: Optional[int] = None
    voice_name: Optional[str] = None
    language_code: Optional[str] = None
    character_count: int = 0

    def get_audio_size_bytes(self) -> int:
        return len(self.audio_content)


@dataclass
class VoiceInfo:
    name: str
    language_code: str
    ssml_gender: str
    natural_sample_rate_hertz: int = 24000

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class VoiceListResponse:
    voices: List[VoiceInfo] = field(default_factory=list)
    locale: Optional[str] = None

    def filter_by_gender(self, gender: str) -> "VoiceListResponse":
        filtered = [v for v in self.voices if v.ssml_gender.upper() == gender.upper()]
        return VoiceListResponse(voices=filtered, locale=self.locale)

    def filter_by_name_pattern(self, pattern: str) -> "VoiceListResponse":
        filtered = [v for v in self.voices if pattern.lower() in v.name.lower()]
        return VoiceListResponse(voices=filtered, locale=self.locale)

    def get_first(self) -> Optional[VoiceInfo]:
        return self.voices[0] if self.voices else None


def normalize_voice_response(raw_voices) -> VoiceListResponse:
    voices = []
    for v in raw_voices:
        voices.append(
            VoiceInfo(
                name=v.name,
                language_code=v.language_codes[0] if v.language_codes else "",
                ssml_gender=v.ssml_gender.name
                if hasattr(v.ssml_gender, "name")
                else str(v.ssml_gender),
                natural_sample_rate_hertz=v.natural_sample_rate_hertz,
            )
        )
    return VoiceListResponse(voices=voices)


def build_ssml(
    text: str,
    voice_name: Optional[str] = None,
    language_code: str = "en-US",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    volume: str = "default",
) -> str:
    prosody_attrs = []
    if speaking_rate != 1.0:
        prosody_attrs.append(f'rate="{speaking_rate}"')
    if pitch != 0.0:
        prosody_attrs.append(f'pitch="{pitch}st"')
    if volume != "default":
        prosody_attrs.append(f'volume="{volume}"')

    prosody = ""
    if prosody_attrs:
        attrs = " ".join(prosody_attrs)
        prosody = f"<prosody {attrs}>{text}</prosody>"
    else:
        prosody = text

    voice_tag = ""
    if voice_name:
        voice_tag = f'<voice name="{voice_name}">'

    ssml = f'<speak lang="{language_code}">{voice_tag}{prosody}{"</voice>" if voice_tag else ""}</speak>'
    return ssml
