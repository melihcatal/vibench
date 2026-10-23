import os
import json
import uuid
from google.cloud import pubsub_v1

from messaging_client import get_publisher, TOPIC_PATH
from messaging_models import SimpleMessage

def batch_publish(messages: list[dict]):
    """
    Publishes a batch of messages to the Google Cloud Pub/Sub topic.

    Args:
        messages: A list of dictionaries, where each dict is a message payload.
    """
    publisher = get_publisher()
    publish_futures = []

    for msg_payload in messages:
        message = SimpleMessage(message_id=str(uuid.uuid4()), payload=msg_payload)
        data = json.dumps(message.to_dict()).encode("utf-8")
        
        # When you publish a message, the client returns a future.
        future = publisher.publish(TOPIC_PATH, data, origin="batch_publish")
        publish_futures.append(future)

    # Wait for all the publish futures to resolve.
    results = [future.result() for future in publish_futures]
    
    print(f"Published {len(results)} messages in a batch.")
    return results
