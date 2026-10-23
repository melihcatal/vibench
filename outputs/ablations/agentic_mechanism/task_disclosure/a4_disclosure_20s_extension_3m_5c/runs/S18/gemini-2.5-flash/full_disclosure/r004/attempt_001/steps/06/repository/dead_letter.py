from google.cloud import pubsub_v1
import json

def send_to_dead_letter(project_id: str, topic_id: str, message_data: dict, attributes: dict = None):
    """Sends a message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        project_id: The Google Cloud project ID.
        topic_id: The ID of the dead-letter topic.
        message_data: The message payload as a dictionary.
        attributes: Optional attributes to include with the message.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    if attributes is None:
        attributes = {}

    data = json.dumps(message_data).encode("utf-8")

    future = publisher.publish(topic_path, data, **attributes)
    print(f"Published message to {topic_path} with ID: {future.result()}")
