import json
import os
from typing import Any, Dict, Iterable, List, Optional

from google.cloud import pubsub_v1

from messaging_client import build_publisher, resolve_topic_path
from messaging_models import BatchPublishResult, MessageEnvelope, normalize_json_payload


def batch_publish(messages: Iterable[Any], attributes_list: Optional[Iterable[Optional[Dict[str, str]]]] = None) -> Dict[str, Any]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    topic_id = os.environ.get("PUBSUB_TOPIC")
    if not project_id or not topic_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT and PUBSUB_TOPIC are required")

    publisher = build_publisher()
    topic_path = resolve_topic_path(project_id, topic_id)
    attrs_iter = list(attributes_list or [])
    futures = []
    items = list(messages)
    for idx, payload in enumerate(items):
        attrs = attrs_iter[idx] if idx < len(attrs_iter) and attrs_iter[idx] else {}
        envelope = MessageEnvelope(payload=normalize_json_payload(payload), attributes=attrs)
        data = json.dumps(envelope.payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        futures.append((envelope.attributes, publisher.publish(topic_path, data=data, **envelope.attributes)))

    results: List[Dict[str, Any]] = []
    for attrs, future in futures:
        results.append({"message_id": future.result(), "attributes": attrs})
    return BatchPublishResult(topic=topic_path, results=results).to_dict()
