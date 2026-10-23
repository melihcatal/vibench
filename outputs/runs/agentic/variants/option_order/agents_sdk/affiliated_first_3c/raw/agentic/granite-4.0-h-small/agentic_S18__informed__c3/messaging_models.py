from typing import TypedDict, List

# Simple event schema used across the flow
class EventPayload(TypedDict):
    id: str
    content: str
    # Extend this class for additional attributes as needed

class PublisherRequest(TypedDict):
    event: EventPayload
    topic: str

class ConsumerPollResult(TypedDict):
    key: str
    value: EventPayload
    partition: int
    offset: int

# Dead-letter payload
class DeadLetterMessage(TypedDict):
    original: EventPayload
    error: str
    timestamp: str
