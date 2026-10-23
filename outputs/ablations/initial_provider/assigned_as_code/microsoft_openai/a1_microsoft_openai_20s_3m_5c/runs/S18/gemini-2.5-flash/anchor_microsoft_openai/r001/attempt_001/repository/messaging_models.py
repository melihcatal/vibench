import json
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class ServiceBusMessagePayload:
    event: Dict[str, Any]
    message_id: Optional[str] = None
    content_type: str = "application/json"

@dataclass
class PublishRequest:
    payload: ServiceBusMessagePayload
    config: Optional[Dict[str, Any]] = None

@dataclass
class ConsumeResponse:
    payload: Dict[str, Any]
    message_id: str
    sequence_number: int
    lock_token: str

@dataclass
class BatchPublishRequest:
    payloads: list[ServiceBusMessagePayload]
    config: Optional[Dict[str, Any]] = None
