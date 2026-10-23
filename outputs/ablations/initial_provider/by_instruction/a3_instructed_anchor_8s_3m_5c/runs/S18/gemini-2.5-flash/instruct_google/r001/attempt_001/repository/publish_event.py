import os
from messaging_client import PubSubClient
from messaging_models import PubSubEvent
from google.cloud.pubsub_v1 import PublisherClient

def publish_event(topic_id: str, event: PubSubEvent):
    client = PubSubClient()
    publisher: PublisherClient = client.get_publisher_client()
    topic_path = client.topic_path(topic_id)

    # Ensure the topic exists, or create it
    try:
        publisher.get_topic(request={"topic": topic_path})
    except Exception as e:
        print(f"Topic {topic_path} does not exist, attempting to create it. Error: {e}")
        publisher.create_topic(request={"name": topic_path})
        print(f"Topic {topic_path} created.")

    future = publisher.publish(topic_path, event.to_json().encode("utf-8"), **event.attributes)
    return future.result()

