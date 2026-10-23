from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class TTSRequest:
    text: str
    voice_id: str
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    use_speaker_boost: bool = True
    language_code: Optional[str] = None

    def to_elevenlabs_kwargs(self) -> Dict[str, Any]:
        kwargs = {
            "text": self.text,
            "voice": self.voice_id,
            "model": self.model_id,
            "output_format": self.output_format,
        }
        voice_settings = {
            "stability": self.stability,
            "similarity_boost": self.similarity_boost,
            "style": self.style,
            "use_speaker_boost": self.use_speaker_boost,
        }
        kwargs["voice_settings"] = voice_settings
        if self.language_code:
            kwargs["language_code"] = self.language_code
        return kwargs


@dataclass
class SSMLRequest:
    ssml: str
    voice_id: str
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    use_speaker_boost: bool = True

    def to_elevenlabs_kwargs(self) -> Dict[str, Any]:
        kwargs = {
            "text": self.ssml,
            "voice": self.voice_id,
            "model": self.model_id,
            "output_format": self.output_format,
        }
        voice_settings = {
            "stability": self.stability,
            "similarity_boost": self.similarity_boost,
            "style": self.style,
            "use_speaker_boost": self.use_speaker_boost,
        }
        kwargs["voice_settings"] = voice_settings
        return kwargs


@dataclass
class TTSResponse:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    model_id: str = ""
    voice_id: str = ""
    character_count: int = 0

    @property
    def audio_size(self) -> int:
        return len(self.audio_bytes)


@dataclass
class VoiceInfo:
    voice_id: str
    name: str
    category: str
    labels: Dict[str, str]
    preview_url: Optional[str] = None


@dataclass
class VoiceSelectionResult:
    selected_voice: VoiceInfo
    locale: str
    all_candidates: List[VoiceInfo] = field(default_factory=list)


def build_ssml(
    text: str,
    voice_name: str = "default",
    rate: str = "medium",
    pitch: str = "default",
    volume: str = "default",
) -> str:
    rate_map = {
        "x-slow": "x-slow",
        "slow": "slow",
        "medium": "medium",
        "fast": "fast",
        "x-fast": "x-fast",
    }
    pitch_map = {
        "x-low": "x-low",
        "low": "low",
        "default": "default",
        "high": "high",
        "x-high": "x-high",
    }
    volume_map = {
        "silent": "silent",
        "x-soft": "x-soft",
        "soft": "soft",
        "medium": "medium",
        "loud": "loud",
        "x-loud": "x-loud",
    }
    rate_val = rate_map.get(rate, "medium")
    pitch_val = pitch_map.get(pitch, "default")
    volume_val = volume_map.get(volume, "medium")
    escaped_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    ssml = f'<speak><voice name="{voice_name}"><prosody rate="{rate_val}" pitch="{pitch_val}" volume="{volume_val}">{escaped_text}</prosody></voice></speak>'
    return ssml


def normalize_audio_bytes(
    raw_audio: bytes, output_format: str = "mp3_44100_128"
) -> bytes:
    return raw_audio
