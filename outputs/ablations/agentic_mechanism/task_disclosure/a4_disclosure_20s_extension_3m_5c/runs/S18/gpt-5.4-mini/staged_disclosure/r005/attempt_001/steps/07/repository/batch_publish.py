import os
import sys
from typing import Any, Dict, Iterable, List, Optional

from google.cloud import pubsub_v1


def _load_messages(argv: List[str]) -> List[Dict[str, Any]]:
    if len(argv) < 2:
        return []
    if len(argv) == 2 and os.path.isfile(argv[1]):
        import json

        with open(argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        raise ValueError("Input file must contain a JSON array of message objects")
    import json

    data = json.loads(argv[1])
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    raise ValueError("Input must be a JSON array of message objects")


def _build_message(msg: Dict[str, Any]) -> pubsub_v1.PubsubMessage:
    data = msg.get("data", "")
    if isinstance(data, str):
        payload = data.encode("utf-8")
    elif isinstance(data, bytes):
        payload = data
    else:
        payload = str(data).encode("utf-8")
    attributes = msg.get("attributes") or {}
    if not isinstance(attributes, dict):
        raise ValueError("attributes must be a dict")
    return pubsub_v1.PubsubMessage(data=payload, attributes={str(k): str(v) for k, v in attributes.items()})


def batch_publish(project_id: str, topic_id: str, messages: Iterable[Dict[str, Any]]) -> List[str]:
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    request = pubsub_v1.PublishRequest(topic=topic_path, messages=[_build_message(m) for m in messages])
    response = publisher.publish(request=request)
    return list(response.message_ids)


def main(argv: List[str]) -> int:
    if len(argv) < 4:
        return 2
    project_id = argv[1]
    topic_id = argv[2]
    messages = _load_messages(argv[2:])
    message_ids = batch_publish(project_id, topic_id, messages)
    for message_id in message_ids:
        print(message_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
