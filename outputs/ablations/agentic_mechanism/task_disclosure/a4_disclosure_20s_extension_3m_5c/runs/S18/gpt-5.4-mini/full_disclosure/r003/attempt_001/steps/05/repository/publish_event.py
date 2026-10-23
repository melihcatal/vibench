import json
import os
from typing import Any, Dict, Optional

from google.api_core.exceptions import GoogleAPICallError
from google.cloud import pubsub_v1


def _get_default_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")


def publish_event(topic_path: str, event: Dict[str, Any], project_id: Optional[str] = None) -> str:
    project_id = project_id or _get_default_project_id()
    if not project_id:
        raise ValueError("project_id is required")
    publisher = pubsub_v1.PublisherClient()
    full_topic = topic_path if topic_path.startswith("projects/") else publisher.topic_path(project_id, topic_path)
    data = json.dumps(event, separators=(",", ":"), sort_keys=True).encode("utf-8")
    future = publisher.publish(full_topic, data=data, content_type="application/json")
    try:
        return future.result()
    except GoogleAPICallError:
        raise


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("topic", help="Pub/Sub topic name or full topic path")
    parser.add_argument("event", help="JSON event payload")
    parser.add_argument("--project-id", default=None)
    args = parser.parse_args()
    event = json.loads(args.event)
    message_id = publish_event(args.topic, event, args.project_id)
    print(message_id)


if __name__ == "__main__":
    main()
