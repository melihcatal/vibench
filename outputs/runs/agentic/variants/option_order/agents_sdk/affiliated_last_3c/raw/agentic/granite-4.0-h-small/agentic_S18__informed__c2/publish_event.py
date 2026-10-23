import os
import json
import google.cloud.pubsub_v1 as pubsub

# Google Cloud Pub/Sub credentials are provided via GOOGLE_APPLICATION_CREDENTIALS env var
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
topic_name = os.getenv('PUBSUB_TOPIC_NAME')

def publish_event(message: dict) -> None:
    """Publish a single JSON event to a Pub/Sub topic.

    Args:
        message (dict): The event payload.
    """
    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    # Convert dict to JSON string
    data = json.dumps(message).encode('utf-8')
    # The publish() call is asynchronous; we wait for the future to complete.
    future = publisher.publish(topic_path, data=data)
    # Optional: block until message is sent
    try:
        future.result()
        print(f"Message published with ID: {future.result()}")
    except Exception as e:
        print(f"Publish failed: {e}")
