import json
from google.cloud import pubsub_v1

from messaging_client import topic_path, TOPIC_ID
from messaging_models import Event

def batch_publish(events: list[Event]) -> list[str]:
    publisher = pubsub_v1.PublisherClient()
    topic = topic_path(TOPIC_ID)
    futures = []
    for event in events:
        data = json.dumps(event.to_dict()).encode('utf-8')
        attributes = {'event_type': event.event_type}
        future = publisher.publish(topic, data, **attributes)
        futures.append(future)
    message_ids = [f.result() for f in futures]
    return message_ids