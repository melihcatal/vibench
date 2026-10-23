import json
from google.cloud import pubsub_v1

from messaging_client import topic_path, TOPIC_ID
from messaging_models import Event

def publish_event(event: Event) -> str:
    publisher = pubsub_v1.PublisherClient()
    topic = topic_path(TOPIC_ID)
    data = json.dumps(event.to_dict()).encode('utf-8')
    api_future = publisher.publish(topic, data)
    message_id = api_future.result()
    return message_id