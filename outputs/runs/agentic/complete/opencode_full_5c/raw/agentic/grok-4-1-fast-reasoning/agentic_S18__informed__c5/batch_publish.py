import json
from datetime import datetime
from uuid import uuid4
from google.cloud import pubsub_v1
from messaging_client import PUBSUB_CONFIG
from messaging_models import MessageEvent, MessagePayload


def batch_publish(events):
    project_id = PUBSUB_CONFIG["project_id"]
    topic_id = PUBSUB_CONFIG["topic_id"]
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    futures = []
    for event in events:
        data = json.dumps(event.model_dump()).encode("utf-8")
        attrs = event.attributes or {}
        future = publisher.publish(topic_path, data, **attrs)
        futures.append(future)
    for future in futures:
        future.result()
    print("Batch published successfully.")


if __name__ == "__main__":
    events = [
        MessageEvent(
            event_id=str(uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            payload=MessagePayload(
                customer_name="Batch1", order_id="B-001", message="First batch message"
            ),
            attributes={"batch_id": "1"},
        ),
        MessageEvent(
            event_id=str(uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            payload=MessagePayload(
                customer_name="Batch2", order_id="B-002", message="Second batch message"
            ),
            attributes={"batch_id": "1"},
        ),
    ]
    batch_publish(events)
