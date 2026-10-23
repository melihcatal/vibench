import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1


@dataclass
class ConsumedEvent:
    message_id: str
    data: bytes
    attributes: Dict[str, str]
    ordering_key: str
    ack_id: Optional[str] = None

    def as_text(self) -> str:
        return self.data.decode("utf-8", errors="replace")

    def as_json(self) -> Any:
        return json.loads(self.as_text())


def consume_one_message(subscription_path: Optional[str] = None, timeout: float = 5.0) -> Optional[ConsumedEvent]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    subscription_path = subscription_path or os.environ.get("PUBSUB_SUBSCRIPTION")
    if not subscription_path:
        raise ValueError("PUBSUB_SUBSCRIPTION or subscription_path is required")

    subscriber = pubsub_v1.SubscriberClient()
    if not subscription_path.startswith("projects/"):
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required when using a short subscription name")
        subscription_path = subscriber.subscription_path(project_id, subscription_path)

    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        },
        timeout=timeout,
    )

    if not response.received_messages:
        return None

    received = response.received_messages[0]
    message = received.message
    return ConsumedEvent(
        message_id=message.message_id,
        data=message.data,
        attributes=dict(message.attributes),
        ordering_key=message.ordering_key,
        ack_id=received.ack_id,
    )


def main() -> None:
    event = consume_one_message()
    if event is None:
        print("no message")
        return
    print(json.dumps({
        "message_id": event.message_id,
        "data": event.as_text(),
        "attributes": event.attributes,
        "ordering_key": event.ordering_key,
    }))


if __name__ == "__main__":
    main()
