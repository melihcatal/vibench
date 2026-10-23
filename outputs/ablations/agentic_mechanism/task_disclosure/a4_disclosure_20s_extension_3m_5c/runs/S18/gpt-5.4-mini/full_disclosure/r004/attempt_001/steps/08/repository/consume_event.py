import json
import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1


def _subscription_path(project_id: str, subscription_name: str) -> str:
    return f"projects/{project_id}/subscriptions/{subscription_name}"


def consume_one_message(project_id: Optional[str] = None, subscription_name: Optional[str] = None, timeout: float = 10.0) -> Dict[str, Any]:
    project_id = project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
    subscription_name = subscription_name or os.environ["PUBSUB_SUBSCRIPTION"]
    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(
        request={"subscription": _subscription_path(project_id, subscription_name), "max_messages": 1},
        timeout=timeout,
    )
    if not response.received_messages:
        return {"received": False, "message": None}
    received = response.received_messages[0]
    message = received.message
    payload: Any = message.data.decode("utf-8", errors="replace") if message.data else ""
    try:
        payload = json.loads(payload)
    except Exception:
        pass
    subscriber.acknowledge(
        request={"subscription": _subscription_path(project_id, subscription_name), "ack_ids": [received.ack_id]}
    )
    return {
        "received": True,
        "message": {
            "message_id": message.message_id,
            "publish_time": message.publish_time.isoformat() if message.publish_time else None,
            "attributes": dict(message.attributes),
            "data": payload,
        },
    }


if __name__ == "__main__":
    print(json.dumps(consume_one_message(), ensure_ascii=False))
