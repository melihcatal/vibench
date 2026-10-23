
import dataclasses
from typing import Literal, Optional

@dataclasses.dataclass
class SpeechRequest:
    text: str
    voice: str = "default"
    audio_format: Literal["mp3", "wav", "ogg"] = "mp3"

@dataclasses.dataclass
class SpeechResponse:
    audio_content: bytes
    audio_format: Literal["mp3", "wav", "ogg"]

def normalize_text(text: str) -> str:
    """
    Normalizes the input text for Text-to-Speech synthesis.
    This could include cleaning, punctuation handling, etc.
    """
    # Example normalization: strip leading/trailing whitespace and replace multiple spaces
    return " ".join(text.strip().split())

def select_voice(voice_name: str) -> str:
    """
    Selects and validates a voice for Text-to-Speech.
    In a real scenario, this would involve looking up available voices
    from a TTS provider.
    """
    # Placeholder for voice selection logic
    available_voices = ["default", "male_1", "female_1"]
    if voice_name in available_voices:
        return voice_name
    else:
        # Fallback to default or raise an error
        return "default"

