from typing import TypedDict, List, Optional


class EventPayload(TypedDict):
    event_id: str
    user_id: str
    data: dict


class ProcessingResult(TypedDict):
    message_id: str
    status: str
    errors: Optional[List[str]]
    processed_at: str
