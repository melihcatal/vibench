from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class Message:
    data: Dict[str, Any]
    attributes: Dict[str, str]
    message_id: Optional[str] = None


@dataclass
class BatchPublishRequest:
    messages: List[Dict[str, Any]]


@dataclass
class BatchPublishResponse:
    message_ids: List[str]


@dataclass
class DeadLetterRequest:
    message_data: Dict[str, Any]
    attributes: Dict[str, str]
    error_details: Optional[str] = None


@dataclass
class DeadLetterResponse:
    message_id: str
