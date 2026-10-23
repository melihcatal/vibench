import json
from typing import Any, Dict, Iterable, List

from google.cloud import pubsub_v1

from messaging_client import build_attributes, load_config, publisher_client, topic_path
from messaging_models import normalize_payload


def publish_batch(events: Iterable[Any]) -> List[str]:
    config = load_config()
    client = publisher_client()
    topic = topic_path(config.project_id, config.topic_id)
    futures = []
    for index, event in enumerate(events):
        payload = normalize_payload(event)
        attrs: Dict[str, str] = build_attributes({"batch_index": index})
        futures.append(client.publish(topic, json.dumps(payload, separators=(",", ":")).encode("utf-8"), **attrs))
    return [future.result() for future in futures]
