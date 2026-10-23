from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class TextModerationRequest:
    text: str
    client_ref_id: Optional[str] = None

@dataclass
class TextModerationResult:
    text: str
    is_unsafe: bool
    scores: Dict[str, float]
    unsafe_spans: List[Dict[str, Any]]

@dataclass
class BatchModerationRequest:
    texts: List[str]
    client_ref_ids: Optional[List[str]] = None

@dataclass
class BatchModerationResult:
    results: List[TextModerationResult]

@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    redacted_spans: List[Dict[str, Any]]
