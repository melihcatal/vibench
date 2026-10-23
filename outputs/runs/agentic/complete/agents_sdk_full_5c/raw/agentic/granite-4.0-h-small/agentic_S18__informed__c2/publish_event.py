import os, json, uuid
from google.cloud import pubsub_v1

# Helper client utilities imported from local module
from messaging_client import PubSubClient
from messaging_models import PubSubMessage

def publish_event(topic_name: str, payload: dict, attr: dict = None):
    """Publish a single JSON event to a Pub/Sub topic.

    Args:
        topic_name (str): Fully qualified topic name (projects/PROJECT/topics/TOPIC).
        payload (dict): Event data as a dict, will be JSON‑encoded.
        attr (dict, optional): Message attributes to attach.
    """
    # Initialise a client wrapper that abstracts credential loading
    client = PubSubClient()
    # Convert payload to JSON string
    data = json.dumps(payload).encode('utf-8')
    message = PubSubMessage(data=data, attributes=attr)
    # Publish using the wrapped client (uses GOOGLE_APPLICATION_CREDENTIALS env var)
    future = client.publish(topic_name, message)
    msg_id = future.result()
    print(f"Published message {msg_id}")

if __name__ == "__main__":
    # Example usage – replace with your own project/topic
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    topic = f"projects/{project_id}/topics/example-topic"
    sample_event = {"event_id": str(uuid.uuid4()), "body": "hello world"}
    publish_event(topic, sample_event)
