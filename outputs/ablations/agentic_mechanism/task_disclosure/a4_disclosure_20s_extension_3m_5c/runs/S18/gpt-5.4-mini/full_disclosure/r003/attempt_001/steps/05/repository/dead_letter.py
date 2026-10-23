import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.api_core.exceptions import GoogleAPICallError
from google.cloud import pubsub_v1


@dataclass
class DeadLetterResult:
    message_id: str
    dead_letter_message_id: str


def _default_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")


def send_to_dead_letter(
    dead_letter_topic: str,
    failed_message: Dict[str, Any],
    project_id: Optional[str] = None,
) -> DeadLetterResult:
    project_id = project_id or _default_project_id()
    if not project_id:
        raise ValueError("project_id is required")

    publisher = pubsub_v1.PublisherClient()
    full_topic = dead_letter_topic if dead_letter_topic.startswith("projects/") else publisher.topic_path(project_id, dead_letter_topic)

    payload = {
        "original_message_id": failed_message.get("message_id"),
        "original_subscription": failed_message.get("subscription"),
        "failure_reason": failed_message.get("failure_reason"),
        "attributes": failed_message.get("attributes", {}),
        "data": failed_message.get("data"),
        "ordering_key": failed_message.get("ordering_key", ""),
    }
    data = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

    future = publisher.publish(full_topic, data=data, content_type="application/json", dead_letter="true")
    try:
        dead_letter_message_id = future.result()
    except GoogleAPICallError:
        raise

    return DeadLetterResult(
        message_id=str(failed_message.get("message_id", "")),
        dead_letter_message_id=dead_letter_message_id,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("topic", help="Pub/Sub dead-letter topic name or full topic path")
    parser.add_argument("message", help="JSON failed message payload")
    parser.add_argument("--project-id", default=None)
    args = parser.parse_args()
    result = send_to_dead_letter(args.topic, json.loads(args.message), args.project_id)
    print(json.dumps({"message_id": result.message_id, "dead_letter_message_id": result.dead_letter_message_id}))


if __name__ == "__main__":
    main()
