import json
import os
from typing import List, Dict, Any, Tuple

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError
from concurrent.futures import as_completed

from messaging_client import get_publisher_client, get_topic_path

def publish_batch(
    publisher: pubsub_v1.PublisherClient,
    topic_path: str,
    messages: List[Tuple[Dict[str, Any], Dict[str, str]]],
):
    """
    Publishes a batch of messages to a Pub/Sub topic.
    The client library handles the actual batching of requests.
    """
    published_message_ids = []
    futures = []

    try:
        for data, attributes in messages:
            payload = json.dumps(data).encode("utf-8")
            # The publish method is non-blocking and returns a Future.
            future = publisher.publish(topic_path, data=payload, **(attributes or {}))
            futures.append(future)
        
        print(f"Published {len(messages)} messages to {topic_path} in a batch.")

        # Wait for all the publish futures to resolve.
        for future in as_completed(futures):
            message_id = future.result()
            published_message_ids.append(message_id)

        print(f"Successfully published message IDs: {published_message_ids}")
        return published_message_ids

    except GoogleAPICallError as e:
        print(f"Error publishing batch to {topic_path}: {e}")
        raise

if __name__ == '__main__':
    # This is an example and will not be executed in the test environment
    # Required environment variables: GOOGLE_PROJECT_ID, MY_TOPIC_ID
    topic_id = os.environ.get("MY_TOPIC_ID")
    if topic_id:
        client = get_publisher_client()
        path = get_topic_path(topic_id)
        message_batch = [
            ({"id": 1, "data": "message one"}, {"source": "batch_script"}),
            ({"id": 2, "data": "message two"}, {"source": "batch_script"}),
            ({"id": 3, "data": "message three"}, None),
        ]
        publish_batch(client, path, message_batch)
    else:
        print("MY_TOPIC_ID environment variable not set. Skipping example.")
