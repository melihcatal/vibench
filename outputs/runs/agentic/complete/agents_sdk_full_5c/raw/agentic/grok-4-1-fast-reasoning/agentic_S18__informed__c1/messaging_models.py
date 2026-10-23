from typing import TypedDict, Dict, Any, List

class PubSubEvent(TypedDict):
    data: Dict[str, Any]
    message_id: str
    attributes: Dict[str, str]

class ProcessingResult(TypedDict):
    message_id: str
    summary: str
    toxicity_score: float
    translated_text: str
    audit_id: str