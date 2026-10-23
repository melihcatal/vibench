
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ModerationCategory:
    category: str
    severity: float

@dataclass
class ModerationResult:
    text: str
    categories: List[ModerationCategory] = field(default_factory=list)
    unsafe_spans: List[Dict[str, Any]] = field(default_factory=list)
    summary: Optional[str] = None
    embedding: Optional[List[float]] = None

@dataclass
class BatchModerationRequest:
    texts: List[str]

@dataclass
class BatchModerationResponse:
    results: List[ModerationResult]

@dataclass
class RedactionRequest:
    text: str
    categories_to_redact: List[str] = field(default_factory=list)

@dataclass
class RedactionResponse:
    redacted_text: str
    unsafe_spans: List[Dict[str, Any]] = field(default_factory=list)
