from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from messaging_client import DEFAULT_TOPIC_ID, topic_path
from messaging_models import MessageEnvelope, PublishRequest, normalize_attributes, normalize_payload


def publish_event(
    payload: Any,
    topic_id: str = DEFAULT_TOPIC_ID,
    attributes: Optional[Dict[str, Any]] = None,
    project_id: Optional[str] = None,
) -> str:
    request = PublishRequest(
        topic=topic_id,
        payload=normalize_payload(payload),
        attributes=normalize_attributes(attributes),
    )
    envelope = MessageEnvelope(message_id=request.message_id, payload=request.payload, attributes=request.attributes)
    publisher = pubsub_v1.PublisherClient()
    future = publisher.publish(
        topic_path(request.topic, project_id),
        envelope.to_json().encode("utf-8"),
        **request.attributes,
    )
    return future.result()


if __name__ == "__main__":
    sample = json.loads(os.getenv("PUBSUB_SAMPLE_PAYLOAD", '{"event":"created","severity":"info"}'))
    print(publish_event(sample))
