import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_config, get_publisher
from messaging_models import PublishRequest, PublishResponse, normalize_attributes


def publish_event(payload, attributes=None, topic_path=None):
    config = get_pubsub_config()
    publisher = get_publisher(config)
    topic_path = topic_path or config.topic_path
    request = PublishRequest(payload=payload, attributes=normalize_attributes(attributes))
    future = publisher.publish(topic_path, json.dumps(request.payload).encode("utf-8"), **request.attributes)
    message_id = future.result()
    return PublishResponse(message_id=message_id, topic_path=topic_path).as_dict()


if __name__ == "__main__":
    data = json.loads(os.environ.get("PUBSUB_EVENT_JSON", "{}"))
    print(json.dumps(publish_event(data), sort_keys=True))
