import json
from messaging_client import PubSubClient


def publish_event(
    topic_id, event_data
):  # publishes a JSON event to a managed Pub/Sub topic
    client = PubSubClient()  # Google Cloud Pub/Sub provider
    json_event = json.dumps(event_data)
    response = client.publish(topic_id, json_event)
    print(f"Published event to {topic_id}: {response}")
