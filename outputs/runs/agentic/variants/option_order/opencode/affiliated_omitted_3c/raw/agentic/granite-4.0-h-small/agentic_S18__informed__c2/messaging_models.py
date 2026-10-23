from typing import TypedDict, List, Dict


class PublishRequest(TypedDict):
    topic_name: str
    event_data: dict


class PublishResponse(TypedDict):
    message_id: str
    status: str


class ConsumeResponse(TypedDict):
    message_id: str
    body: str
    attributes: Dict[str, str]


class BatchPublishRequest(TypedDict):
    topic_name: str
    messages: List[dict]
    batch_id: str


class BatchPublishResponse(TypedDict):
    batch_id: str
    sent_count: int
    failed_count: int


class DeadLetterRequest(TypedDict):
    source_subscription: str
    dlq_topic: str
    message_id: str
