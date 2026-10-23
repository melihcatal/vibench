import os
import json
from concurrent.futures import Future
from typing import List, Dict

from google.cloud import pubsub_v1
from messaging_client import get_publisher, TOPIC_PATH
from messaging_models import SimpleMessage

def publish_batch(messages: List[SimpleMessage]):
    """Publishes a batch of messages to a Pub/Sub topic."""
    publisher = get_publisher()
    publish_futures: List[Future] = []

    def get_callback(f: Future, data: str):
        def callback(f: Future):
            try:
                print(f"Successfully published message with ID: {f.result()}")
            except Exception as e:
                print(f"Failed to publish message: {data}, error: {e}")
        return callback

    for message in messages:
        data = json.dumps(message.data).encode("utf-8")
        
        # The Pub/Sub client library automatically handles batching.
        # When you publish a message, the client adds it to a batch and sends it 
        # to the service after a certain number of messages or a time interval.
        future = publisher.publish(
            TOPIC_PATH, 
            data, 
            messageId=message.message_id, 
            origin="batch_publish"
        )
        future.add_done_callback(get_callback(future, str(message.data)))
        publish_futures.append(future)

    # Wait for all the publish futures to resolve
    results = [f.result() for f in publish_futures]
    print(f"Published {len(results)} messages in a batch.")
    return results

