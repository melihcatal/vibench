import dataclasses
from typing import List, Dict, Any, Optional

@dataclasses.dataclass
class TextModerationRequest:
    text: str
    language_code: str = "en"

@dataclasses.dataclass
class TextModerationResponse:
    toxicity: Dict[str, Any]
    content_safe: bool

@dataclasses.dataclass
class BatchModerationRequest:
    texts: List[str]
    language_code: str = "en"

@dataclasses.dataclass
class BatchModerationResponse:
    results: List[TextModerationResponse]

@dataclasses.dataclass
class RedactionRequest:
    text: str
    categories_to_redact: List[str]
    redaction_character: str = "*"

@dataclasses.dataclass
class RedactionResponse:
    redacted_text: str
    unsafe_spans: List[Dict[str, Any]]

@dataclasses.dataclass
class ModerationDecision:
    text: str
    is_safe: bool
    reasons: List[str]
    scores: Dict[str, Any]
