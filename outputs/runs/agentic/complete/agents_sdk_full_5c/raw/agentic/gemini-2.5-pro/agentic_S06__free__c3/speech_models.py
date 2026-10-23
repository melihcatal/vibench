from dataclasses import dataclass
from typing import List

@dataclass
class Voice:
    """Represents a TTS voice."""
    name: str
    language_codes: List[str]
    ssml_gender: str

@dataclass
class SynthesisRequest:
    """Represents a request for speech synthesis."""
    text: str
    voice_name: str
    language_code: str
