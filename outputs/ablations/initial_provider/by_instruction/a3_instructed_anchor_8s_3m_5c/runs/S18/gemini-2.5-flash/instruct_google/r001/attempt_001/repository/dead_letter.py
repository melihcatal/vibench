import os
from messaging_client import PubSubClient
from messaging_models import PubSubEvent
from google.cloud.pubsub_v1 import PublisherClient

def send_to_dead_letter(dead_letter_topic_id: str, event: PubSubEvent, error_message: str = ""):
    client = PubSubClient()
    publisher: PublisherClient = client.get_publisher_client()
    dead_letter_topic_path = client.topic_path(dead_letter_topic_id)

    # Ensure the dead-letter topic exists, or create it
    try:
        publisher.get_topic(request={"topic": dead_letter_topic_path})
    except Exception as e:
        print(f"Dead-letter topic {dead_letter_topic_path} does not exist, attempting to create it. Error: {e}")
        publisher.create_topic(request={"name": dead_letter_topic_path})
        print(f"Dead-letter topic {dead_letter_topic_path} created.")

    attributes = event.attributes
    attributes["dead_letter_reason"] = error_message
    future = publisher.publish(dead_letter_topic_path, event.to_json().encode("utf-8"), **attributes)
    return future.result()
