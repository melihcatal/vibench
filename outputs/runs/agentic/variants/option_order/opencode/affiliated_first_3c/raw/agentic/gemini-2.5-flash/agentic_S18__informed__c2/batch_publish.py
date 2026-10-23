import json
import os

from messaging_client import PubSubClient
from messaging_models import PubsubMessage, BatchPublishRequest, BatchPublishResponse


def batch_publish(topic_id: str, request: BatchPublishRequest) -> BatchPublishResponse:
    client = PubSubClient()
    topic_path = client.get_topic_path(topic_id)

    futures = []
    for message in request.messages:
        future = client.publisher.publish(
            topic_path, message.data, **message.attributes
        )
        futures.append(future)

    message_ids = []
    for future in futures:
        message_ids.append(
            future.result()
        )  # Wait for each publish operation to complete

    return BatchPublishResponse(message_ids=message_ids)


if __name__ == "__main__":
    # Example Usage (requires GOOGLE_CLOUD_PROJECT environment variable set)
    # and a Pub/Sub topic named 'my-topic'
    topic_id = "my-topic"

    messages_to_publish = [
        PubsubMessage(
            data=json.dumps({"order_id": "123", "item": "Laptop"}).encode("utf-8"),
            attributes={"event_type": "order_created"},
        ),
        PubsubMessage(
            data=json.dumps({"order_id": "124", "item": "Mouse"}).encode("utf-8"),
            attributes={"event_type": "order_created"},
        ),
        PubsubMessage(
            data=json.dumps({"order_id": "125", "item": "Keyboard"}).encode("utf-8"),
            attributes={"event_type": "order_created"},
        ),
    ]

    request = BatchPublishRequest(messages=messages_to_publish)
    response = batch_publish(topic_id, request)

    print(f"Published batch of messages with IDs: {response.message_ids}")
