import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path, load_messaging_config
from messaging_models import DeadLetterRequest, PublishResult, normalize_attributes, serialize_event


def dead_letter(payload):
    config = load_messaging_config()
    client = get_publisher_client()
    topic_path = get_topic_path(client, config.project_id, config.dead_letter_topic_id)
    request = DeadLetterRequest.from_payload(payload)
    data = serialize_event(request.record)
    future = client.publish(topic_path, data=data, **normalize_attributes(request.attributes))
    message_id = future.result()
    return PublishResult(message_id=message_id, topic=topic_path, attributes=request.attributes, payload=request.record)


if __name__ == '__main__':
    print(dead_letter(json.loads('{"error":"processing_failed","text":"bad payload"}')).to_json())
