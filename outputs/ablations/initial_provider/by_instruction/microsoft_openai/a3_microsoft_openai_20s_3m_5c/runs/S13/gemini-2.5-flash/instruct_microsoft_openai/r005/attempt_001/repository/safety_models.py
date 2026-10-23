from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ModerationRequest:
    text_content: str

@dataclass
class ModerationResponse:
    categories: Dict[str, int] = field(default_factory=dict)
    reasoning: str = ""

@dataclass
class BatchModerationRequest:
    texts: List[str]

@dataclass
class BatchModerationResponse:
    results: List[Dict[str, Any]] = field(default_factory=list)
