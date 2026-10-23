import json
from typing import Dict, Any, Optional

# ---------------------------------------------------------------------------
# Message request/response models for Pub/Sub integration
# ---------------------------------------------------------------------------


class PublishRequest:
    """
    Payload container for publishing a single message.
    """

    def __init__(self, topic: str, payload: Dict[str, Any], key: Optional[str] = None):
        self.topic = topic
        self.payload = payload
        self.key = key  # optional partitioning key

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "payload": self.payload,
            "key": self.key,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PublishRequest":
        return PublishRequest(
            topic=data["topic"], payload=data["payload"], key=data.get("key")
        )


class PublishResponse:
    """
    Dummy response container – Confluent producer returns None.
    """

    def __init__(self):
        self.success = True
        self.error = None

    @classmethod
    def from_result(cls, success: bool, error: Optional[Exception]):
        instance = cls()
        instance.success = success
        instance.error = error
        return instance


class ConsumeResponse:
    """
    Wrapper for a consumed message payload.
    """

    def __init__(self, msg: Optional[str]):
        self.message = json.loads(msg) if msg else None
        self.error = None if msg else Exception("No message returned")

    def __bool__(self):
        return self.message is not None


class DeadLetterPayload:
    """
    Structure persisted to DLQ.
    """

    def __init__(
        self, original_topic: str, key: Optional[str], raw_message: str, error: str
    ):
        self.original_topic = original_topic
        self.key = key
        self.raw_message = raw_message
        self.error = error
        self.timestamp = int(
            json.loads(json.dumps(int.__new__(int)))
        )  # placeholder for now

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_topic": self.original_topic,
            "key": self.key,
            "raw_message": self.raw_message,
            "error": self.error,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "DeadLetterPayload":
        return DeadLetterPayload(
            original_topic=data["original_topic"],
            key=data.get("key"),
            raw_message=data["raw_message"],
            error=data["error"],
        )
