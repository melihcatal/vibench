import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_subscriber
from messaging_models import EventMessage


def consume_event(subscription_id: str = None, timeout: float = 5.0) -> dict:
    """Consume one message from Google Cloud Pub/Sub subscription."""
    if subscription_id is None:
        subscription_id = os.environ.get(
            "PUBSUB_SUBSCRIPTION_ID", "customer-events-sub"
        )

    subscriber, project_id = get_pubsub_subscriber()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1}
    )

    if not response.received_messages:
        print("No messages available")
        return None

    message = response.received_messages[0]
    data = json.loads(message.message.data.decode("utf-8"))

    event_message = EventMessage.from_dict(data)

    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [message.ack_id]}
    )

    print(f"Consumed message {message.message.message_id}")
    return {
        "message_id": message.message.message_id,
        "data": event_message.to_dict(),
        "attributes": dict(message.message.attributes),
    }


if __name__ == "__main__":
    result = consume_event()
    if result:
        print(f"Received message: {json.dumps(result, indent=2)}")
