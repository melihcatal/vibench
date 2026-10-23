from typing import TypedDict


class EventPayload(TypedDict):
    message_id: str
    content: str
    user_id: str
