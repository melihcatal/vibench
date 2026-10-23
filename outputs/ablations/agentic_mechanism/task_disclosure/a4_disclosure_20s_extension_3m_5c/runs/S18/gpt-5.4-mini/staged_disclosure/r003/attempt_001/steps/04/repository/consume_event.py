import json
import os
import sys

from google.cloud import pubsub_v1


def consume_one_message() -> int:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION")
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
    if not subscription_id:
        raise RuntimeError("PUBSUB_SUBSCRIPTION is required")

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        },
        timeout=10,
    )

    if not response.received_messages:
        return 0

    received = response.received_messages[0]
    message = received.message
    payload = message.data.decode("utf-8") if message.data else ""

    try:
        parsed = json.loads(payload) if payload else None
    except json.JSONDecodeError:
        parsed = payload

    print(json.dumps({"message_id": message.message_id, "payload": parsed}, ensure_ascii=False))

    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [received.ack_id],
        }
    )
    return 0


if __name__ == "__main__":
    sys.exit(consume_one_message())
