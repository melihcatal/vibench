import json
import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1


def _get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def consume_one_message() -> Dict[str, Any]:
    project_id = _get_env("GOOGLE_CLOUD_PROJECT")
    subscription_id = _get_env("PUBSUB_SUBSCRIPTION_ID")
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1, "return_immediately": True}
    )
    if not response.received_messages:
        return {"received": False, "message": None}

    received = response.received_messages[0]
    message = received.message
    payload_text = message.data.decode("utf-8", errors="replace") if message.data else ""
    attributes = dict(message.attributes)
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [received.ack_id]}
    )
    return {
        "received": True,
        "message": {
            "message_id": message.message_id,
            "payload": payload_text,
            "attributes": attributes,
            "publish_time": message.publish_time.isoformat() if message.publish_time else None,
        },
    }


if __name__ == "__main__":
    print(json.dumps(consume_one_message(), ensure_ascii=False))
