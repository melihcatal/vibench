import os
from typing import List
from messaging_client import PubSubClient
from messaging_models import PubSubEvent
from google.cloud.pubsub_v1 import PublisherClient

def batch_publish(topic_id: str, events: List[PubSubEvent]):
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

    futures = []
    for event in events:
        future = publisher.publish(topic_path, event.to_json().encode("utf-8"), **event.attributes)
        futures.append(future)

    # Wait for all the publish futures to resolve synchronously
    results = [future.result() for future in futures]
    return results
