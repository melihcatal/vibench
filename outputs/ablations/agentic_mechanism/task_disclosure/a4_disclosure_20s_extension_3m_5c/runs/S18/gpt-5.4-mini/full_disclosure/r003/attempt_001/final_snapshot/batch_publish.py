import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence

from google.api_core.exceptions import GoogleAPICallError
from google.cloud import pubsub_v1


PUBSUB_API_HOSTNAME = "pubsub.googleapis.com"


@dataclass
class BatchPublishResult:
    message_id: str
    client_token: Optional[str] = None


def _default_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")


def _normalize_messages(messages: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for message in messages:
        if "data" not in message:
            raise ValueError("each message must include data")
        normalized.append(message)
    return normalized


def publish_batch(
    topic_path: str,
    messages: Sequence[Dict[str, Any]],
    project_id: Optional[str] = None,
) -> List[BatchPublishResult]:
    project_id = project_id or _default_project_id()
    if not project_id:
        raise ValueError("project_id is required")

    publisher = pubsub_v1.PublisherClient(client_options={"api_endpoint": PUBSUB_API_HOSTNAME})
    full_topic = topic_path if topic_path.startswith("projects/") else publisher.topic_path(project_id, topic_path)

    normalized_messages = _normalize_messages(messages)
    futures = []
    for message in normalized_messages:
        data = message["data"]
        if isinstance(data, str):
            data = data.encode("utf-8")
        elif isinstance(data, (dict, list)):
            data = json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
        elif not isinstance(data, (bytes, bytearray)):
            raise TypeError("message data must be bytes, string, dict, or list")

        attributes = dict(message.get("attributes", {}))
        if "message_id" in message:
            attributes.setdefault("message_id", str(message["message_id"]))
        if message.get("ordering_key"):
            attributes.setdefault("ordering_key", str(message["ordering_key"]))

        futures.append((message.get("client_token"), publisher.publish(full_topic, data=bytes(data), **attributes)))

    results: List[BatchPublishResult] = []
    for client_token, future in futures:
        try:
            message_id = future.result()
        except GoogleAPICallError:
            raise
        results.append(BatchPublishResult(message_id=message_id, client_token=client_token))
    return results


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("topic", help="Pub/Sub topic name or full topic path")
    parser.add_argument("messages", help="JSON array of messages with data and optional attributes/message_id")
    parser.add_argument("--project-id", default=None)
    args = parser.parse_args()
    results = publish_batch(args.topic, json.loads(args.messages), args.project_id)
    print(json.dumps([{"message_id": result.message_id, "client_token": result.client_token} for result in results]))


if __name__ == "__main__":
    main()
