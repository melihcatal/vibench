import json
from google.cloud import pubsub_v1
from messaging_client import get_topic_path

def publish_event(event: dict):
    """
    publishes a JSON event to a managed messaging topic or queue
    """
    topic_path = get_topic_path()
    publisher = pubsub_v1.PublisherClient()
    data = json.dumps(event).encode('utf-8')
    future = publisher.publish(topic_path, data)
    message_id = future.result()
    print(f"Published {message_id}")
    return message_id