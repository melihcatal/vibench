from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class PubsubMessage:
    data: Dict[str, Any]
    message_id: str
    publish_time: str
    attributes: Optional[Dict[str, str]] = None

@dataclass
class PublishResponse:
    message_id: str

@dataclass
class ConsumeResponse:
    message: PubsubMessage
    ack_id: str

@dataclass
class BatchPublishRequest:
    messages: list[Dict[str, Any]]
    topic_id: str
    project_id: str

@dataclass
class BatchPublishResponse:
    message_ids: list[str]
