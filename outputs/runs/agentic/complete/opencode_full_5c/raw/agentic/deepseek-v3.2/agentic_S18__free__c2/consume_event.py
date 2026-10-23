import os
from google.cloud import pubsub_v1
import json
from typing import Dict, Any, Optional
import time


def consume_event(
    subscription_id: str = None, timeout: float = 5.0
) -> Optional[Dict[str, Any]]:
    """Consume one message from Google Cloud Pub/Sub subscription."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    if subscription_id is None:
        subscription_id = os.environ.get(
            "PUBSUB_SUBSCRIPTION_ID", "customer-events-sub"
        )

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    received_message = None

    def callback(message):
        nonlocal received_message
        data = json.loads(message.data.decode("utf-8"))
        received_message = {
            "data": data,
            "message_id": message.message_id,
            "attributes": dict(message.attributes),
            "publish_time": message.publish_time,
        }
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull_future.result(timeout=timeout)
    except Exception:
        streaming_pull_future.cancel()

    subscriber.close()
    return received_message


if __name__ == "__main__":
    try:
        message = consume_event(timeout=10.0)
        if message:
            print(f"Consumed message ID: {message['message_id']}")
            print(f"Message data: {json.dumps(message['data'], indent=2)}")
        else:
            print("No messages available")
    except Exception as e:
        print(f"Failed to consume event: {e}")
