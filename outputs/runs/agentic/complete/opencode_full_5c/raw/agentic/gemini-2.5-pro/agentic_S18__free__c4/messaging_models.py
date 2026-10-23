from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Message:
    message_id: str
    data: Dict[str, Any]
    attributes: Dict[str, str]


@dataclass
class ProcessingResult:
    message_id: str
    status: str
    summary: str = ""
    safety_scores: Dict[str, float] = None
    translated_text: str = ""
    audit_record_id: str = ""
