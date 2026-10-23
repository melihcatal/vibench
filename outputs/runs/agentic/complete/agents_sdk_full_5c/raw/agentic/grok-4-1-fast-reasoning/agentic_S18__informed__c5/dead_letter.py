import json
from google.cloud import pubsub_v1

from messaging_client import topic_path, DEAD_LETTER_TOPIC_ID
from messaging_models import Event

def send_to_dead_letter(event: Event, error: str):
    publisher = pubsub_v1.PublisherClient()
    topic = topic_path(DEAD_LETTER_TOPIC_ID)
    data = json.dumps(event.to_dict()).encode('utf-8')
    attributes = {'original_error': error}
    api_future = publisher.publish(topic, data, **attributes)
    api_future.result()