import json
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import load_config, publisher_client, topic_path
from messaging_models import PublishEventRequest, normalize_attributes, normalize_payload


def publish_event(request: PublishEventRequest) -> str:
    cfg = load_config()
    client = publisher_client()
    topic = topic_path(cfg.topic_id)
    body = normalize_payload(request.payload)
    message = {
        "event_type": request.event_type,
        "payload": body,
    }
    data = json.dumps(message, separators=(",", ":")).encode("utf-8")
    future = client.publish(
        topic,
        data,
        event_type=request.event_type,
        **normalize_attributes(request.attributes),
    )
    return future.result()
