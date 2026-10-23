import json
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import build_attributes, load_config, publisher_client, topic_path
from messaging_models import normalize_payload


def publish_event(event: Any, attributes: Dict[str, Any] | None = None) -> str:
    config = load_config()
    client = publisher_client()
    topic = topic_path(config.project_id, config.topic_id)
    payload = normalize_payload(event)
    data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    future = client.publish(topic, data, **build_attributes(attributes))
    return future.result()
