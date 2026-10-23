import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import EventMessage

def publish_event(project_id, topic_name, payload):
    """Publish a single JSON event to a Pub/Sub topic.

    Args:
        project_id (str): GCP project ID.
        topic_name (str): Pub/Sub topic name.
        payload (dict): JSON-serializable event data.
    """
    # Load credentials from env var as required by google-cloud libraries
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    publisher = get_pubsub_client()
    message = EventMessage(data=payload).to_json()
    # The topic must be fully qualified: projects/{project_id}/topics/{topic_name}
    topic_path = f"projects/{project_id}/topics/{topic_name}"
    future = publisher.publish(topic_path, data=message.encode('utf-8'))
    # Block on publish
    result = future.result()
    print(f"Published event with message ID: {result}")
