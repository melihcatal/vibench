import json
import os

from google.cloud import pubsub_v1
from messaging_client import PubSubClient
from messaging_models import BatchPublishRequest, BatchPublishResponse

def batch_publish_events(request: BatchPublishRequest) -> BatchPublishResponse:
    client = PubSubClient(request.project_id)
    topic_path = client.get_topic_path(request.topic_id)

    futures = []
    for message_payload in request.messages:
        # Ensure each message in the batch has a unique identifier if needed, or attributes.
        # For this example, we're just publishing the payload as is.
        future = client.publisher.publish(topic_path, json.dumps(message_payload).encode("utf-8"))
        futures.append(future)
    
    message_ids = []
    for future in futures:
        try:
            message_ids.append(future.result(timeout=30))
        except Exception as e:
            # Handle individual message publishing failures if necessary
            print(f"Error publishing message: {e}")
            message_ids.append("failed") # Or a more robust error indicator
    
    client.publisher.stop()
    return BatchPublishResponse(message_ids=message_ids)
