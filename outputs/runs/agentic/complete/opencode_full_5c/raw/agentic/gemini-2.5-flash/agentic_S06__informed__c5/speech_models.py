from dataclasses import dataclass
from typing import Optional


@dataclass
class Voice:
    voice_id: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None


@dataclass
class SynthesisRequest:
    text: str
    voice_id: str
    model_id: str = "eleven_multilingual_v2"


@dataclass
class SSMLSynthesisRequest:
    ssml: str
    voice_id: str
    model_id: str = "eleven_multilingual_v2"
