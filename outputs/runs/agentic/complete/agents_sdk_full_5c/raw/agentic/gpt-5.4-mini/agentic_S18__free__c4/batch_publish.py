import json
from typing import Iterable, List

from messaging_client import load_config, publisher_client, topic_path
from messaging_models import BatchPublishRequest, PublishEventRequest, normalize_attributes, normalize_payload


def publish_batch(request: BatchPublishRequest) -> List[str]:
    cfg = load_config()
    client = publisher_client()
    topic = topic_path(cfg.topic_id)
    futures = []
    for index, item in enumerate(request.messages):
        payload = normalize_payload(item.payload)
        data = json.dumps({"event_type": item.event_type, "payload": payload}, separators=(",", ":")).encode("utf-8")
        attrs = normalize_attributes(item.attributes)
        attrs["batch_index"] = str(index)
        futures.append(client.publish(topic, data, event_type=item.event_type, **attrs))
    return [future.result() for future in futures]
