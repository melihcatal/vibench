from messaging_client import PubSubClient
from messaging_models import BatchMessage, PublishResponse
import os
from typing import List


def batch_publish(topic_id: str, messages: List[BatchMessage]) -> PublishResponse:
    """
    Publishes a batch of messages to a Google Cloud Pub/Sub topic.
    """
    client = PubSubClient()
    batch_messages = [
        {
            "data": message.data,
            "attributes": message.attributes,
        }
        for message in messages
    ]
    message_ids = client.publish_batch(topic_id, batch_messages)
    return PublishResponse(message_ids=message_ids)


if __name__ == "__main__":
    topic_id = os.getenv("PUBSUB_TOPIC_ID")
    messages = [
        BatchMessage(
            data={"event_type": "user_action", "user_id": "12345", "action": "click"}
        ),
        BatchMessage(
            data={"event_type": "user_action", "user_id": "67890", "action": "purchase"}
        ),
    ]
    response = batch_publish(topic_id, messages)
    print(f"Published batch messages with IDs: {response.message_ids}")
