import json
from google.cloud import pubsub_v1
from messaging_client import TOPIC_PATH


def batch_publish(events_data: list[dict]) -> list[str]:
    publisher = pubsub_v1.PublisherClient()
    message_ids = []
    for event_data in events_data:
        data = json.dumps(event_data).encode("utf-8")
        future = publisher.publish(TOPIC_PATH, data)
        message_id = future.result()
        message_ids.append(message_id)
    return message_ids
