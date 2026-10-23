import json
import sys

from messaging_client import encode_json, publisher_client, topic_path
from messaging_models import normalize_payload


def publish_event(topic: str, payload: object, attributes: dict | None = None) -> str:
    client = publisher_client()
    data = normalize_payload(payload)
    future = client.publish(topic_path(topic), encode_json(data), **(attributes or {}))
    return future.result()


if __name__ == "__main__":
    topic = sys.argv[1]
    payload = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    print(publish_event(topic, payload))
