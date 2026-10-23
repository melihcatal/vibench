import json
import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1


def _publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def publish_event(topic_path: str, event: Dict[str, Any], attributes: Optional[Dict[str, str]] = None) -> str:
    client = _publisher_client()
    data = json.dumps(event, separators=(",", ":")).encode("utf-8")
    future = client.publish(topic_path, data, **(attributes or {}))
    return future.result()


def main() -> None:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    topic_id = os.environ["PUBSUB_TOPIC"]
    topic_path = _publisher_client().topic_path(project_id, topic_id)
    payload = os.environ.get("EVENT_JSON", "{}")
    event = json.loads(payload)
    attributes_json = os.environ.get("EVENT_ATTRIBUTES", "{}")
    attributes = json.loads(attributes_json)
    message_id = publish_event(topic_path, event, attributes)
    print(message_id)


if __name__ == "__main__":
    main()
