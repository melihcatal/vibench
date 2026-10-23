import json
import os
import sys
from typing import Any, Dict, List

from google.cloud import pubsub_v1


def _parse_message(entry: Any) -> Dict[str, Any]:
    if isinstance(entry, str):
        try:
            entry = json.loads(entry)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON message entry: {entry}") from exc
    if not isinstance(entry, dict):
        raise ValueError("Each message must be a JSON object")
    if "data" not in entry:
        raise ValueError("Each message must include a 'data' field")
    data = entry["data"]
    if isinstance(data, str):
        data = data.encode("utf-8")
    elif not isinstance(data, (bytes, bytearray)):
        data = json.dumps(data).encode("utf-8")
    attrs = entry.get("attributes") or {}
    if not isinstance(attrs, dict):
        raise ValueError("'attributes' must be an object if provided")
    msg = {"data": data, "attributes": {str(k): str(v) for k, v in attrs.items()}}
    if "message_id" in entry:
        msg["message_id"] = str(entry["message_id"])
    return msg


def batch_publish(topic_path: str, messages: List[Dict[str, Any]]) -> List[str]:
    publisher = pubsub_v1.PublisherClient()
    futures = []
    for message in messages:
        futures.append(
            publisher.publish(
                topic_path,
                message["data"],
                **message.get("attributes", {}),
                message_id=message["message_id"] if "message_id" in message else None,
            )
        )
    return [future.result() for future in futures]


def main() -> int:
    if len(sys.argv) < 3:
        print(
            "Usage: python batch_publish.py <project_id> <topic_name> '<json_messages>'",
            file=sys.stderr,
        )
        return 1

    project_id = sys.argv[1]
    topic_name = sys.argv[2]
    raw_messages = sys.argv[3] if len(sys.argv) > 3 else "[]"

    messages_input = json.loads(raw_messages)
    if not isinstance(messages_input, list):
        raise ValueError("Messages input must be a JSON list")

    messages = [_parse_message(entry) for entry in messages_input]
    topic_path = pubsub_v1.PublisherClient().topic_path(project_id, topic_name)
    ids = batch_publish(topic_path, messages)
    print(json.dumps({"message_ids": ids}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
