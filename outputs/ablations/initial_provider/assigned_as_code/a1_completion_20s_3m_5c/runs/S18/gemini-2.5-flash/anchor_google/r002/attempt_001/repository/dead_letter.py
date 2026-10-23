import json
import os

from google.cloud import pubsub_v1
from messaging_client import PubSubClient
from messaging_models import PublishResponse

def send_to_dead_letter_topic(payload: dict, project_id: str, dead_letter_topic_id: str) -> PublishResponse:
    client = PubSubClient(project_id)
    topic_path = client.get_topic_path(dead_letter_topic_id)

    future = client.publisher.publish(topic_path, json.dumps(payload).encode("utf-8"))
    try:
        return PublishResponse(message_id=future.result(timeout=30))
    finally:
        client.publisher.stop()
