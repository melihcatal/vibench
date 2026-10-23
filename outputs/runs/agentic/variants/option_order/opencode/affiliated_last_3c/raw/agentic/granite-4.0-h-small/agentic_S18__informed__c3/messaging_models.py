import json
from typing import Any, Dict


class EventPayload:
    """Normalize event payload to a consistent dict representation."""

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "EventPayload":
        return cls(**raw)

    def __init__(self, **kwargs):
        self.data = {k: v for k, v in kwargs.items()}

    def to_dict(self) -> Dict[str, Any]:
        return self.data


class ConsumedMessage:
    """Wrap a consumed Pub/Sub message for easier handling."""

    @classmethod
    def from_dict(cls, raw: dict) -> "ConsumedMessage":
        return cls(**raw)

    def __init__(self, **kwargs):
        self.data = kwargs

    def to_dict(self) -> dict:
        return self.data


class InvalidMessage:
    """Representation of a message to be dead-lettered."""

    @classmethod
    def from_dict(cls, raw: dict) -> "InvalidMessage":
        return cls(**raw)

    def __init__(self, payload: dict, reason: str):
        self.payload = payload
        self.reason = reason

    def to_dict(self) -> dict:
        return {"payload": self.payload, "reason": self.reason}
