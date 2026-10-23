from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class MessageEvent:
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

@dataclass
class ProcessedResult:
    summary: str
    is_safe: bool
    translated: str
    audit_id: str