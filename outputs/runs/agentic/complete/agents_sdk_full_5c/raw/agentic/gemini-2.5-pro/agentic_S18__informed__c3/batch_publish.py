
import os
import json
from concurrent.futures import as_completed
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, project_id, topic_id
from messaging_models import EventPayload

def publish_batch(payloads: list[EventPayload]):
    """Publishes a batch of messages to a Google Cloud Pub/Sub topic."""
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(project_id, topic_id)

    publish_futures = []
    for payload in payloads:
        data = payload.model_dump_json().encode("utf-8")
        # The client library automatically batches messages
        future = publisher.publish(topic_path, data, message_id=payload.request_id)
        publish_futures.append(future)

    message_ids = []
    for future in as_completed(publish_futures):
        message_id = future.result()
        message_ids.append(message_id)
        print(f"Published message ID: {message_id}")

    return message_ids

if __name__ == '__main__':
    # This is an example, not part of the required functionality.
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        sample_payloads = [
            EventPayload(request_id=f"req-{i}", user_id=f"user-{i*10}", data={"value": i})
            for i in range(5)
        ]
        publish_batch(sample_payloads)
