"""
speech_models.py - Local request, response, and normalization helpers for Text-to-Speech.

Defines Pydantic-like data classes and helper functions for normalizing
Azure Cognitive Services TTS requests and responses.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import base64
import json


@dataclass
class TTSRequest:
    """Normalized TTS request payload for Azure Cognitive Services."""
    text: str
    voice_name: str = "en-US-AriaNeural"
    locale: str = "en-US"
    output_format: str = "audio-16khz-32kbitrate-mono-mp3"
    rate: str = "+0%"
    pitch: str = "+0Hz"
    volume: str = "default"
    ssml: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)

    def to_ssml(self) -> str:
        """
        Convert request to Azure-compatible SSML format.

        Uses the Microsoft SSML namespace and structure required by
        Azure Cognitive Services Speech Service.
        """
        if self.ssml:
            return self.ssml

        ssml = (
            '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
            f'xml:lang="{self.locale}">'
            f'<voice name="{self.voice_name}">'
            f'<prosody rate="{self.rate}" pitch="{self.pitch}" volume="{self.volume}">'
            f'{_escape_xml(self.text)}'
            f'</prosody>'
            f'</voice>'
            f'</speak>'
        )
        return ssml

    def to_rest_payload(self) -> str:
        """Generate the SSML payload body for Azure REST API synthesis call."""
        return self.to_ssml()


@dataclass
class TTSResponse:
    """Normalized response from Azure TTS synthesis."""
    audio_bytes: bytes = b""
    content_type: str = "audio/mpeg"
    duration_ms: float = 0.0
    request_id: str = ""
    voice_name: str = ""
    audio_format: str = "mp3"
    error_message: Optional[str] = None
    status_code: int = 200

    def is_success(self) -> bool:
        """Check if the synthesis response indicates success."""
        return self.status_code == 200 and self.audio_bytes and not self.error_message

    def to_base64(self) -> str:
        """Encode audio bytes to base64 string."""
        return base64.b64encode(self.audio_bytes).decode("utf-8") if self.audio_bytes else ""

    def save_to_file(self, filepath: str) -> None:
        """Write audio bytes to a local file."""
        with open(filepath, "wb") as f:
            f.write(self.audio_bytes)


@dataclass
class VoiceInfo:
    """Normalized voice metadata from Azure Voice List API."""
    name: str
    locale: str
    gender: str = ""
    style_list: List[str] = field(default_factory=list)
    sample_rate_hertz: int = 24000
    voice_type: str = "Neural"
    status: str = "GA"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "locale": self.locale,
            "gender": self.gender,
            "style_list": self.style_list,
            "sample_rate_hertz": self.sample_rate_hertz,
            "voice_type": self.voice_type,
            "status": self.status,
        }


@dataclass
class SynthesisConfig:
    """Configuration container for synthesis parameters."""
    azure_region: str = "eastus"
    azure_key: str = ""
    default_voice: str = "en-US-AriaNeural"
    default_locale: str = "en-US"
    default_format: str = "audio-16khz-32kbitrate-mono-mp3"
    timeout_seconds: int = 30


def normalize_locale(locale: str) -> str:
    """
    Normalize a locale string to Azure-compatible format.

    Args:
        locale: Locale string like 'en_US' or 'en-us'.

    Returns:
        Normalized Azure locale like 'en-US'.
    """
    return locale.replace("_", "-").strip().title()


def pick_voice_for_locale(locale: str, voices: List[VoiceInfo], preferred_gender: str = "") -> Optional[str]:
    """
    Select a voice name matching the target locale.

    Args:
        locale: Target locale (e.g., 'en-US').
        voices: List of available VoiceInfo objects.
        preferred_gender: Optional gender filter ('Male' or 'Female').

    Returns:
        Voice name string or None if no match found.
    """
    normalized = normalize_locale(locale)
    candidates = [v for v in voices if v.locale == normalized]
    if preferred_gender:
        candidates = [v for v in candidates if v.gender == preferred_gender]
    return candidates[0].name if candidates else None


def parse_azure_voice_list_response(raw_json: str) -> List[VoiceInfo]:
    """
    Parse Azure Voice List API JSON response into VoiceInfo objects.

    The Azure /cognitiveservices/voices/list endpoint returns a JSON array.

    Args:
        raw_json: Raw JSON string from Azure voices list endpoint.

    Returns:
        List of VoiceInfo objects.
    """
    data = json.loads(raw_json)
    voices = []
    for item in data:
        voice = VoiceInfo(
            name=item.get("ShortName", ""),
            locale=item.get("Locale", ""),
            gender=item.get("Gender", ""),
            style_list=item.get("StyleList", []),
            voice_type=item.get("VoiceType", "Neural"),
            status=item.get("Status", "GA"),
        )
        voices.append(voice)
    return voices


def _escape_xml(text: str) -> str:
    """Escape special XML characters in text for SSML."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text
