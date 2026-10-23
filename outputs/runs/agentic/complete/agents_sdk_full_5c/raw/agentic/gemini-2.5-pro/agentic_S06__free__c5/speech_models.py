from dataclasses import dataclass
from typing import List

@dataclass
class SpeechRequest:
    """Represents a basic request for speech synthesis."""
    text: str
    language_code: str
    voice_name: str

@dataclass
class Voice:
    """Represents a text-to-speech voice."""
    name: str
    language_codes: List[str]
    ssml_gender: str
