from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SpeechRequest:
    """Represents a request for speech synthesis."""
    text: Optional[str] = None
    ssml: Optional[str] = None
    language_code: str = "en-US"
    voice_name: str = "en-US-Standard-C"


@dataclass
class Voice:
    """Represents a Text-to-Speech voice."""
    name: str
    language_codes: List[str]
    ssml_gender: str
