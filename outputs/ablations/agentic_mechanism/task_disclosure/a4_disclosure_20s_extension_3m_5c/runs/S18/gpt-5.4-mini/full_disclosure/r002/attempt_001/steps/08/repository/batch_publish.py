import os
from typing import Any, Dict, List, Optional

from google.cloud import pubsub_v1


def _publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def _message_data(message: Dict[str, Any]) -> bytes:
    data = message.get("data", "")
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode("utf-8")
    return str(data).encode("utf-8")


def publish_batch(
    topic_path: str,
    messages: List[Dict[str, Any]],
    ordering_key: Optional[str] = None,
) -> List[str]:
    publisher = _publisher()
    futures = []
    for message in messages:
        attrs = dict(message.get("attributes") or {})
        if "id" in message:
            attrs.setdefault("id", str(message["id"]))
        data = _message_data(message)
        msg = pubsub_v1.PubsubMessage(data=data, attributes=attrs)
        kwargs = {}
        if ordering_key:
            kwargs["ordering_key"] = ordering_key
        futures.append(publisher.publish(topic_path, msg.data, **attrs, **kwargs))
    return [future.result() for future in futures]


def main() -> None:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    topic_id = os.environ.get("PUBSUB_TOPIC")
    if not project_id or not topic_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT and PUBSUB_TOPIC are required")
    topic_path = _publisher().topic_path(project_id, topic_id)
    messages = [{"id": "1", "data": "first"}, {"id": "2", "data": "second", "attributes": {"source": "batch"}}]
    publish_batch(topic_path, messages)


if __name__ == "__main__":
    main()
