import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import EventMessage

def batch_publish(project_id, topic_name, events):
    """Publish a batch of JSON events to a Pub/Sub topic.",
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    publisher = get_pubsub_client()
    topic_path = f"projects/{project_id}/topics/{topic_name}"
    # Prepare messages: each event is turned into a Pub/Sub Message
    messages = []
    for payload in events:
        message = EventMessage(data=payload).to_json()
        messages.append(pubsub_v1.types.PubsubMessage(data=message.encode('utf-8')))
    # Publish all at once
    future = publisher.publish(topic_path, messages=messages)
    result = future.result()
    print(f"Batch published {len(messages)} messages, message ID: {result}." if result else "Batch publish completed.")
