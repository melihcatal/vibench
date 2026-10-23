from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Voice:
    """Represents a voice model with metadata."""

    id: str
    name: str
    language_code: str
    language_name: str
    gender: str
    engine: str


@dataclass
class SynthesisRequest:
    """Request payload for text-to-speech synthesis."""

    text: str
    voice_id: str
    text_type: str = "text"  # or "ssml"
    sample_rate: Optional[str] = None
    engine: Optional[str] = None


@dataclass
class SynthesisResponse:
    """Response from text-to-speech synthesis."""

    audio_bytes: bytes
    content_type: str = "audio/mpeg"


def normalize_voice_list(voices_data: Dict[str, Any]) -> List[Voice]:
    """Normalize Amazon Polly voice data into a list of Voice objects."""
    voices = []
    for voice in voices_data.get("Voices", []):
        voices.append(
            Voice(
                id=voice["Id"],
                name=voice["Name"],
                language_code=voice["LanguageCode"],
                language_name=voice.get("LanguageName", ""),
                gender=voice["Gender"],
                engine=voice.get("SupportedEngines", ["standard"])[0],
            )
        )
    return voices
