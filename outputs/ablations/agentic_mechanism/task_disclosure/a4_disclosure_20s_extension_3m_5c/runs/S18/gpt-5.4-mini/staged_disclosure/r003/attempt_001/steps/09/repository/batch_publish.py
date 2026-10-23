import argparse
import json
import os
from typing import Any, Dict, List, Optional

from google.cloud import pubsub_v1


def _parse_attributes(raw: Optional[str]) -> Dict[str, str]:
    if not raw:
        return {}
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("attributes must be a JSON object")
    return {str(k): str(v) for k, v in data.items()}


def _parse_message(item: Any) -> Dict[str, Any]:
    if isinstance(item, str):
        try:
            item = json.loads(item)
        except json.JSONDecodeError:
            return {"data": item}
    if not isinstance(item, dict):
        raise ValueError("each message must be a JSON object or string")
    return item


def publish_batch(project_id: str, topic_id: str, messages: List[Dict[str, Any]]) -> List[str]:
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    futures = []
    for message in messages:
        data = message.get("data", "")
        if not isinstance(data, str):
            data = json.dumps(data, separators=(",", ":"))
        payload = data.encode("utf-8")
        attributes = message.get("attributes") or {}
        if not isinstance(attributes, dict):
            raise ValueError("attributes must be a JSON object")
        message_id = message.get("id")
        if message_id is not None:
            attributes = {**attributes, "id": str(message_id)}
        futures.append(publisher.publish(topic_path, payload, **{str(k): str(v) for k, v in attributes.items()}))
    return [future.result() for future in futures]


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish a batch of messages to Google Cloud Pub/Sub.")
    parser.add_argument("--project-id", default=os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT"))
    parser.add_argument("--topic-id", required=True)
    parser.add_argument("--messages", required=True, help="JSON array of messages with optional id, data, and attributes")
    args = parser.parse_args()

    if not args.project_id:
        raise SystemExit("--project-id or GOOGLE_CLOUD_PROJECT is required")

    raw_messages = json.loads(args.messages)
    if not isinstance(raw_messages, list):
        raise SystemExit("--messages must be a JSON array")
    messages = [_parse_message(item) for item in raw_messages]
    message_ids = publish_batch(args.project_id, args.topic_id, messages)
    print(json.dumps({"message_ids": message_ids}))


if __name__ == "__main__":
    main()
