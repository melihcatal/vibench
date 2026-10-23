from __future__ import annotations

import json
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import load_config, publisher_client, topic_path
from messaging_models import PublishRequest, build_envelope


def publish_event(event: Dict[str, Any], project_id: str | None = None) -> str:
    config = load_config(project_id)
    envelope = build_envelope(PublishRequest(payload=event, attributes={"source": "publish_event.py"}))
    client = publisher_client()
    future = client.publish(
        topic_path(config),
        envelope.to_json_bytes(),
        **envelope.attributes,
        ordering_key=envelope.ordering_key,
    )
    return future.result()


if __name__ == "__main__":
    sample = {"event_type": "customer.created", "data": {"customer_id": "123", "segment": "gold"}}
    print(json.dumps({"provider": "google.cloud.pubsub_v1", "provider_message_id": publish_event(sample)}, ensure_ascii=False))
