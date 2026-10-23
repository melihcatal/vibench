import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_config, get_publisher
from messaging_models import DeadLetterRequest, normalize_attributes


def dead_letter(payload, reason, attributes=None, dead_letter_topic_path=None):
    config = get_pubsub_config()
    publisher = get_publisher(config)
    dead_letter_topic_path = dead_letter_topic_path or config.dead_letter_topic_path
    request = DeadLetterRequest(payload=payload, reason=reason, attributes=normalize_attributes(attributes))
    body = json.dumps(request.as_dict()).encode("utf-8")
    message_id = publisher.publish(dead_letter_topic_path, body, **request.attributes).result()
    return {"message_id": message_id, "dead_letter_topic_path": dead_letter_topic_path}
