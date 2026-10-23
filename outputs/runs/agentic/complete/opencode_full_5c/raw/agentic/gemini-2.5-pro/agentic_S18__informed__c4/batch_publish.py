import json
from typing import List
from messaging_client import (
    get_publisher_client,
    get_topic_path,
    PROJECT_ID,
    TOPIC_ID,
)
from messaging_models import EventPayload


def publish_batch(events: List[EventPayload]):
    publisher = get_publisher_client()
    topic_path = get_topic_path(publisher, PROJECT_ID, TOPIC_ID)

    futures = []

    for event in events:
        data = json.dumps(event).encode("utf-8")
        future = publisher.publish(
            topic_path, data, correlation_id=event.get("event_id", "")
        )
        futures.append(future)

    message_ids = [future.result() for future in futures]
    print(f"Published {len(message_ids)} messages in a batch.")
    return message_ids
