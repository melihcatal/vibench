import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path, load_messaging_config
from messaging_models import BatchPublishRequest, BatchPublishResult, normalize_attributes, serialize_event


def batch_publish(payload):
    config = load_messaging_config()
    client = get_publisher_client()
    topic_path = get_topic_path(client, config.project_id, config.topic_id)
    request = BatchPublishRequest.from_payload(payload)
    futures = []
    for item in request.messages:
        futures.append(client.publish(topic_path, data=serialize_event(item.body), **normalize_attributes(item.attributes)))
    return BatchPublishResult(message_ids=[future.result() for future in futures], topic=topic_path)


if __name__ == '__main__':
    print(batch_publish(json.loads('{"messages":[{"id":"1","text":"one"},{"id":"2","text":"two"}]}')).to_json())
