from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from google.cloud import pubsub_v1

from messaging_client import DEFAULT_TOPIC_ID, topic_path
from messaging_models import BatchPublishRequest, MessageEnvelope, PublishRequest, normalize_attributes, normalize_payload


def batch_publish(
    messages: Iterable[Dict[str, Any]],
    topic_id: str = DEFAULT_TOPIC_ID,
    project_id: Optional[str] = None,
) -> List[str]:
    requests: List[PublishRequest] = []
    for item in messages:
        requests.append(
            PublishRequest(
                topic=topic_id,
                payload=normalize_payload(item.get("payload", item)),
                attributes=normalize_attributes(item.get("attributes")),
                message_id=str(item.get("message_id") or item.get("id") or ""),
            )
        )

    batch = BatchPublishRequest(topic=topic_id, messages=requests)
    publisher = pubsub_v1.PublisherClient()
    results: List[str] = []
    for request in batch.messages:
        envelope = MessageEnvelope(message_id=request.message_id or request.payload.get("id", ""), payload=request.payload, attributes=request.attributes)
        results.append(
            publisher.publish(
                topic_path(batch.topic, project_id),
                envelope.to_json().encode("utf-8"),
                **request.attributes,
            ).result()
        )
    return results
