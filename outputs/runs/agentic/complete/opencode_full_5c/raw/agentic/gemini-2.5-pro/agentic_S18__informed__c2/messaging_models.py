from typing import TypedDict, Any, Dict


class MessagePayload(TypedDict):
    event_id: str
    user_id: str
    data: Dict[str, Any]


class ProcessingResult(TypedDict):
    message_id: str
    status: str
    summary: str
    is_safe: bool
    translated_text: str
    audit_id: str
