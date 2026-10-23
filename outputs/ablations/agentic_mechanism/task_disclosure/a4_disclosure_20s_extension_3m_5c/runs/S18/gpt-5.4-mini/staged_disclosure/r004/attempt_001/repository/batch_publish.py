import json
import os
import sys
from typing import Iterable, List, Mapping, Optional

from google.cloud import pubsub_v1


def _parse_message(item: Mapping[str, object]) -> tuple[bytes, dict]:
    data = item.get("data", "")
    attributes = item.get("attributes", {})
    if not isinstance(attributes, dict):
        raise ValueError("attributes must be a mapping")
    if isinstance(data, str):
        payload = data.encode("utf-8")
    elif isinstance(data, (bytes, bytearray)):
        payload = bytes(data)
    else:
        payload = json.dumps(data, separators=(",", ":")).encode("utf-8")
    return payload, {str(k): str(v) for k, v in attributes.items()}


def publish_batch(project_id: str, topic_id: str, messages: Iterable[Mapping[str, object]]) -> List[str]:
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    futures = []
    for message in messages:
        payload, attributes = _parse_message(message)
        futures.append(publisher.publish(topic_path, payload, **attributes))
    return [future.result() for future in futures]


def main(argv: Optional[List[str]] = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("Usage: batch_publish.py '[{""data"": ""..."", ""attributes"": {}}]'", file=sys.stderr)
        return 2
    messages = json.loads(args[0])
    if not isinstance(messages, list):
        raise ValueError("messages must be a JSON array")
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    topic_id = os.environ["PUBSUB_TOPIC"]
    message_ids = publish_batch(project_id, topic_id, messages)
    print(json.dumps({"message_ids": message_ids}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
