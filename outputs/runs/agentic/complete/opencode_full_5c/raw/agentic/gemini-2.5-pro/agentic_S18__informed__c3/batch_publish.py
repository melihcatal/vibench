import os
from concurrent.futures import as_completed
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import Message


def publish_batch(messages: list[Message]):
    publisher = get_publisher_client()
    topic_id = os.environ.get("GCP_TOPIC_ID", "my-topic")
    topic_path = get_topic_path(topic_id)

    publish_futures = []

    for message in messages:
        future = publisher.publish(
            topic_path, message.to_json(), **(message.attributes or {})
        )
        publish_futures.append(future)

    # Wait for all the publish futures to resolve
    message_ids = [future.result() for future in as_completed(publish_futures)]
    return message_ids


if __name__ == "__main__":
    messages_to_send = [
        Message(
            data={"event_id": "evt-001", "value": 100}, attributes={"type": "sale"}
        ),
        Message(
            data={"event_id": "evt-002", "value": 200}, attributes={"type": "sale"}
        ),
        Message(
            data={"event_id": "evt-003", "value": 50}, attributes={"type": "refund"}
        ),
    ]
    print(f"Publishing batch of {len(messages_to_send)} messages.")
    ids = publish_batch(messages_to_send)
    print(f"Published messages with IDs: {ids}")
