import json
from typing import Any, Dict

from messaging_client import build_attributes, load_config, publisher_client, topic_path
from messaging_models import normalize_payload


def send_dead_letter(message: Any, attributes: Dict[str, Any] | None = None) -> str:
    config = load_config()
    client = publisher_client()
    topic = topic_path(config.project_id, config.dead_letter_topic)
    payload = normalize_payload(message)
    data = json.dumps({"dead_letter": payload}, separators=(",", ":")).encode("utf-8")
    return client.publish(topic, data, **build_attributes(attributes)).result()
