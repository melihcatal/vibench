from google.cloud import pubsub_v1

from messaging_client import encode_json, publisher_client, topic_path
from messaging_models import build_batch_request


def batch_publish(topic: str, payloads, attributes_list=None):
    request = build_batch_request(topic, payloads, attributes_list)
    client = publisher_client()
    topic_name = topic_path(request.topic)
    futures = []
    for message in request.messages:
        futures.append(client.publish(topic_name, encode_json(message.payload), **message.attributes))
    return {"provider": "google.pubsub_v1", "topic": topic_name, "message_ids": [future.result() for future in futures]}
