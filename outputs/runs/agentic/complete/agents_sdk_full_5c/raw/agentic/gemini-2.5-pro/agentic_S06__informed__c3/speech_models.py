from dataclasses import dataclass
from typing import List

@dataclass
class Voice:
    name: str
    language_codes: List[str]
    ssml_gender: str

@dataclass
class SynthesisRequest:
    text: str
    voice_name: str
    language_code: str
