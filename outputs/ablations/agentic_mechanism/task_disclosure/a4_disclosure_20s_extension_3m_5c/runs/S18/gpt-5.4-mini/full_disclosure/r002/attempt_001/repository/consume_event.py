import json
import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1


def consume_event(subscription_path: Optional[str] = None, timeout: float = 10.0) -> Dict[str, Any]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION")
    if subscription_path is None:
        if not project_id or not subscription_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT/GCP_PROJECT and PUBSUB_SUBSCRIPTION are required")
        subscription_path = f"projects/{project_id}/subscriptions/{subscription_id}"

    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(request={"subscription": subscription_path, "max_messages": 1}, timeout=timeout)
    if not response.received_messages:
        return {"message": None, "ack_id": None, "subscription": subscription_path}

    received = response.received_messages[0]
    message = received.message
    payload = message.data.decode("utf-8") if message.data else ""
    attributes = dict(message.attributes)

    try:
        decoded_payload = json.loads(payload) if payload else None
    except json.JSONDecodeError:
        decoded_payload = payload

    subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [received.ack_id]})

    return {
        "subscription": subscription_path,
        "ack_id": received.ack_id,
        "message": {
            "message_id": message.message_id,
            "publish_time": message.publish_time.isoformat() if message.publish_time else None,
            "attributes": attributes,
            "data": decoded_payload,
        },
    }


if __name__ == "__main__":
    result = consume_event()
    print(json.dumps(result, default=str))
