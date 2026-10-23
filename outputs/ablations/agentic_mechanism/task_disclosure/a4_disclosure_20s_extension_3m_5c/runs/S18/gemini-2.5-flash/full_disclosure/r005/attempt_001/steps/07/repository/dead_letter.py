
from google.cloud import pubsub_v1
import json

def send_to_dead_letter(project_id: str, topic_id: str, message_data: dict):
    """Sends a failed message to a Google Cloud Pub/Sub dead-letter topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    message_json = json.dumps(message_data)
    message_bytes = message_json.encode("utf-8")

    try:
        future = publisher.publish(topic_path, message_bytes)
        message_id = future.result()
        print(f"Message {message_id} published to dead-letter topic {topic_id}.")
        return message_id
    except Exception as e:
        print(f"Error publishing message to dead-letter topic: {e}")
        raise

