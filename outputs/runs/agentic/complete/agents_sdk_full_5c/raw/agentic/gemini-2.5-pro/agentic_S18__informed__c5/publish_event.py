import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher, TOPIC_PATH
from messaging_models import SimpleMessage

def publish_message(message: SimpleMessage):
    """Publishes a single message to a Pub/Sub topic."""
    publisher = get_publisher()

    # Data must be a bytestring
    data = json.dumps(message.data).encode("utf-8")

    future = publisher.publish(TOPIC_PATH, data, messageId=message.message_id)
    print(f"Published message ID: {future.result()}")
    return future.result()
