import json
import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1


def publish_event(project_id: str, topic_id: str, event: Dict[str, Any], ordering_key: Optional[str] = None) -> str:
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = json.dumps(event, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    future = publisher.publish(topic_path, data=data, ordering_key=ordering_key or "")
    return future.result()


def _load_event_from_env() -> Dict[str, Any]:
    raw = os.environ.get("EVENT_JSON", "{}")
    return json.loads(raw)


def main() -> None:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    topic_id = os.environ["PUBSUB_TOPIC"]
    ordering_key = os.environ.get("PUBSUB_ORDERING_KEY")
    event = _load_event_from_env()
    message_id = publish_event(project_id, topic_id, event, ordering_key=ordering_key)
    print(message_id)


if __name__ == "__main__":
    main()
