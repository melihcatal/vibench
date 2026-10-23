from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Voice:
    id: str
    name: str
    language_code: str
    language_name: str
    gender: str


@dataclass
class SynthesisRequest:
    text: str
    voice_id: str = "Joanna"
    output_format: str = "mp3"
    ssml: bool = False


@dataclass
class SynthesisResponse:
    audio_content: bytes
    content_type: str


def normalize_voice_list(voices_data: Dict[str, Any]) -> List[Voice]:
    voices = []
    for voice in voices_data.get("Voices", []):
        voices.append(
            Voice(
                id=voice["Id"],
                name=voice["Name"],
                language_code=voice["LanguageCode"],
                language_name=voice.get("LanguageName", ""),
                gender=voice["Gender"],
            )
        )
    return voices
