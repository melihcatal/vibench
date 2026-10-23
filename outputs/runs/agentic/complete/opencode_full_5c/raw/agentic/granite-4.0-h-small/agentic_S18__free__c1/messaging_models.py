from typing import TypedDict, Literal


class MessagePayload(TypedDict):
    event_type: str
    data: dict
    timestamp: str


class PublishResponse(TypedDict):
    message_id: str
    status: Literal["OK", "FAILED"]


class ConsumeResponse(TypedDict):
    message_id: str
    payload: MessagePayload


class DeadLetterResult(TypedDict):
    original_message_id: str
    dead_letter_topic: str
    result: Literal["SENT", "ERROR"]
