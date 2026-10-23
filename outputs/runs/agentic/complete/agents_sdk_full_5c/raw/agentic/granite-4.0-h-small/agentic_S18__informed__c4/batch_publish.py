import os
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client
from messaging_models import normalize_event

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
topic_name = os.getenv('BATCH_TOPIC', 'my-topic')

def publish_batch(events):
    """Publish a list of JSON events as a batch to Google Cloud Pub/Sub.

    Args:
        events (list[dict]): List where each element is a JSON‑serializable event.
    """
    publisher = get_publisher_client()
    messages = []
    for ev in events:
        payload = normalize_event(ev)
        data = str(payload).encode('utf-8')
        # Provide an explicit message ID or attribute if desired
        messages.append(pubsub_v1.types.PubsubMessage(data=data))
    # atomic publish of all messages
    try:
        future = publisher.publish(topic_name, messages=messages)
        future.result()  # wait for completion
        print(f"Batch of {len(events)} messages published."
              f" Result: {future.result()}")
    except Exception as e:
        print(f"Error publishing batch: {e}")
