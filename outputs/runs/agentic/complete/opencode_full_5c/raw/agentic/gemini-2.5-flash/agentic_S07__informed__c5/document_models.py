from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class DocumentExtractionResult:
    text: str = ""
    layout: List[Dict[str, Any]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    key_values: List[Dict[str, str]] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)
