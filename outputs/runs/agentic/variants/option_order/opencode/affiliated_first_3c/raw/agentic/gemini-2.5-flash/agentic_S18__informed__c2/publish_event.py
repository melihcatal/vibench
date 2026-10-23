import json
import os

from messaging_client import PubSubClient
from messaging_models import PubsubMessage, PublishResponse


def publish_event(topic_id: str, message: PubsubMessage) -> PublishResponse:
    client = PubSubClient()
    topic_path = client.get_topic_path(topic_id)

    future = client.publisher.publish(topic_path, message.data, **message.attributes)
    message_id = future.result()

    return PublishResponse(message_ids=[message_id])


if __name__ == "__main__":
    # Example Usage (requires GOOGLE_CLOUD_PROJECT environment variable set)
    # and a Pub/Sub topic named 'my-topic'
    topic_id = "my-topic"
    event_data = {"key": "value", "event_type": "test_event"}
    event_attributes = {"origin": "example_script"}

    message = PubsubMessage(
        data=json.dumps(event_data).encode("utf-8"), attributes=event_attributes
    )

    response = publish_event(topic_id, message)
    print(f"Published message with ID: {response.message_ids[0]}")
