import os
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

from google.cloud import pubsub_v1


@dataclass(frozen=True)
class PubSubConfig:
    project_id: str
    topic_id: Optional[str] = None
    subscription_id: Optional[str] = None

    @classmethod
    def from_env(cls) -> "PubSubConfig":
        return cls(
            project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
            topic_id=os.getenv("PUBSUB_TOPIC"),
            subscription_id=os.getenv("PUBSUB_SUBSCRIPTION"),
        )

    @property
    def topic_path(self) -> str:
        if not self.topic_id:
            raise ValueError("PUBSUB_TOPIC is required")
        return pubsub_v1.PublisherClient().topic_path(self.project_id, self.topic_id)

    @property
    def subscription_path(self) -> str:
        if not self.subscription_id:
            raise ValueError("PUBSUB_SUBSCRIPTION is required")
        return pubsub_v1.SubscriberClient().subscription_path(self.project_id, self.subscription_id)


class MessagingClient:
    def __init__(self, config: Optional[PubSubConfig] = None):
        self.config = config or PubSubConfig.from_env()
        self._publisher = pubsub_v1.PublisherClient()
        self._subscriber = pubsub_v1.SubscriberClient()

    @staticmethod
    def _encode_message(data: Any) -> bytes:
        if isinstance(data, bytes):
            return data
        if isinstance(data, bytearray):
            return bytes(data)
        if isinstance(data, str):
            return data.encode("utf-8")
        return str(data).encode("utf-8")

    @staticmethod
    def _normalize_attributes(attributes: Optional[Mapping[str, Any]]) -> Dict[str, str]:
        return {str(k): str(v) for k, v in (attributes or {}).items()}

    def publish(self, data: Any, attributes: Optional[Mapping[str, Any]] = None) -> str:
        topic_path = self.config.topic_path
        payload = self._encode_message(data)
        attrs = self._normalize_attributes(attributes)
        return self._publisher.publish(topic_path, payload, **attrs).result()

    def receive_one(self, timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        subscription_path = self.config.subscription_path
        response = self._subscriber.pull(
            request={"subscription": subscription_path, "max_messages": 1},
            timeout=timeout,
        )
        if not response.received_messages:
            return None
        received = response.received_messages[0]
        message = received.message
        self._subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": [received.ack_id]}
        )
        return {
            "message_id": message.message_id,
            "data": message.data.decode("utf-8", errors="replace"),
            "attributes": dict(message.attributes),
            "publish_time": message.publish_time.isoformat() if message.publish_time else None,
        }


def get_client(config: Optional[PubSubConfig] = None) -> MessagingClient:
    return MessagingClient(config=config)
