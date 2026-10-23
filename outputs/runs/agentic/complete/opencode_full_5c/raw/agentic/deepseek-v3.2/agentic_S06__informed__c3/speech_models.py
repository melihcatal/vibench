from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from enum import Enum


class VoiceGender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NEUTRAL = "Neutral"


class VoiceType(str, Enum):
    STANDARD = "Standard"
    NEURAL = "Neural"
    PREMIUM = "Premium"


class AudioFormat(str, Enum):
    RIFF_16KHZ_16BIT_MONO_PCM = "riff-16khz-16bit-mono-pcm"
    RIFF_24KHZ_16BIT_MONO_PCM = "riff-24khz-16bit-mono-pcm"
    RIFF_48KHZ_16BIT_MONO_PCM = "riff-48khz-16bit-mono-pcm"
    RAW_16KHZ_16BIT_MONO_PCM = "raw-16khz-16bit-mono-pcm"
    RAW_24KHZ_16BIT_MONO_PCM = "raw-24khz-16bit-mono-pcm"
    RAW_48KHZ_16BIT_MONO_PCM = "raw-48khz-16bit-mono-pcm"


@dataclass
class VoiceInfo:
    name: str
    locale: str
    gender: VoiceGender
    voice_type: VoiceType
    supported_styles: List[str] = field(default_factory=list)

    @classmethod
    def from_azure_voice(cls, azure_voice):
        gender_map = {
            "Male": VoiceGender.MALE,
            "Female": VoiceGender.FEMALE,
            "Neutral": VoiceGender.NEUTRAL,
        }

        voice_type_map = {
            "Standard": VoiceType.STANDARD,
            "Neural": VoiceType.NEURAL,
            "Premium": VoiceType.PREMIUM,
        }

        return cls(
            name=azure_voice.short_name,
            locale=azure_voice.locale,
            gender=gender_map.get(
                azure_voice.gender.name if azure_voice.gender else "Neutral",
                VoiceGender.NEUTRAL,
            ),
            voice_type=voice_type_map.get(
                azure_voice.voice_type.name if azure_voice.voice_type else "Standard",
                VoiceType.STANDARD,
            ),
            supported_styles=azure_voice.style_list
            if hasattr(azure_voice, "style_list")
            else [],
        )


@dataclass
class SynthesisRequest:
    text: str
    voice_name: str = "en-US-JennyNeural"
    output_format: AudioFormat = AudioFormat.RIFF_16KHZ_16BIT_MONO_PCM
    rate: str = "medium"
    pitch: str = "medium"
    volume: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_ssml(self) -> str:
        return f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{self.voice_name[:5]}">
    <voice name="{self.voice_name}">
        <prosody rate="{self.rate}" pitch="{self.pitch}" volume="{self.volume}">
            {self.text}
        </prosody>
    </voice>
</speak>"""


@dataclass
class SynthesisResponse:
    audio_data: bytes
    request: SynthesisRequest
    voice_used: str
    audio_format: AudioFormat
    duration_seconds: Optional[float] = None
    sample_rate: int = 16000
    sample_width: int = 2
    channels: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AudioInfo:
    size_bytes: int
    format: str
    sample_rate: int
    sample_width: int
    channels: int
    duration_seconds: Optional[float] = None
    bitrate_kbps: Optional[float] = None

    @property
    def bitrate(self) -> Optional[float]:
        if self.duration_seconds and self.duration_seconds > 0:
            return (self.size_bytes * 8) / (self.duration_seconds * 1000)
        return None


@dataclass
class BatchSynthesisRequest:
    items: List[SynthesisRequest]
    concurrency_limit: int = 5
    output_directory: Optional[str] = None
    naming_pattern: str = "synthesis_{index}.wav"


@dataclass
class BatchSynthesisResult:
    successes: List[SynthesisResponse]
    failures: List[Dict[str, Any]]
    total_items: int
    successful_items: int
    failed_items: int


def normalize_voice_name(voice_name: str) -> str:
    if not voice_name:
        return "en-US-JennyNeural"

    voice_name = voice_name.strip()

    if "-" not in voice_name:
        return f"en-US-{voice_name}"

    return voice_name


def validate_synthesis_request(request: SynthesisRequest) -> List[str]:
    errors = []

    if not request.text or not request.text.strip():
        errors.append("Text cannot be empty")

    if len(request.text) > 5000:
        errors.append("Text exceeds maximum length of 5000 characters")

    if not request.voice_name:
        errors.append("Voice name cannot be empty")

    try:
        AudioFormat(request.output_format)
    except ValueError:
        errors.append(f"Invalid audio format: {request.output_format}")

    valid_rates = ["x-slow", "slow", "medium", "fast", "x-fast", "default"]
    if request.rate not in valid_rates and not request.rate.endswith("%"):
        errors.append(f"Invalid rate value: {request.rate}")

    valid_pitches = ["x-low", "low", "medium", "high", "x-high", "default"]
    if request.pitch not in valid_pitches and not request.pitch.endswith("%"):
        errors.append(f"Invalid pitch value: {request.pitch}")

    if not 0.0 <= request.volume <= 2.0:
        errors.append(f"Volume must be between 0.0 and 2.0, got {request.volume}")

    return errors
