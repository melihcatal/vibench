import json
import os
import uuid
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path, load_messaging_config
from messaging_models import PublishRequest, PublishResult, normalize_attributes, normalize_payload_text, serialize_event


def publish_event(payload):
    config = load_messaging_config()
    client = get_publisher_client()
    topic_path = get_topic_path(client, config.project_id, config.topic_id)
    request = PublishRequest.from_payload(payload)
    data = serialize_event(request.event)
    future = client.publish(topic_path, data=data, **normalize_attributes(request.attributes))
    message_id = future.result()
    return PublishResult(message_id=message_id, topic=topic_path, attributes=request.attributes, payload=normalize_payload_text(request.event))


if __name__ == '__main__':
    event = json.loads(os.environ.get('EVENT_JSON', '{"id":"' + str(uuid.uuid4()) + '","text":"hello"}'))
    result = publish_event(event)
    print(result.to_json())
