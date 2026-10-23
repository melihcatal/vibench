import dataclasses
from typing import List

@dataclasses.dataclass
class TextSafetyRequest:
    text_content: str
    client_id: str = "default"

@dataclasses.dataclass
class SafetyAttribute:
    category: str
    score: float

@dataclasses.dataclass
class TextSafetyResponse:
    decision: str
    attributes: List[SafetyAttribute]

def normalize_text(text: str) -> str:
    # Placeholder for text normalization logic
    # This could include lowercasing, removing punctuation, etc.
    return text.strip().lower()
