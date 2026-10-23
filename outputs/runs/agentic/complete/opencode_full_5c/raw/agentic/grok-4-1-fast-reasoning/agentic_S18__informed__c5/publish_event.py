import json
import os
from datetime import datetime
from uuid import uuid4
from google.cloud import pubsub_v1
from messaging_client import PUBSUB_CONFIG
from messaging_models import MessageEvent, MessagePayload


def publish_event(event: MessageEvent):
    project_id = PUBSUB_CONFIG["project_id"]
    topic_id = PUBSUB_CONFIG["topic_id"]
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = json.dumps(event.model_dump()).encode("utf-8")
    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")


if __name__ == "__main__":
    event = MessageEvent(
        event_id=str(uuid4()),
        timestamp=datetime.utcnow().isoformat(),
        payload=MessagePayload(
            customer_name="John Doe",
            order_id="ORD-123",
            message="Order confirmation: Your pizza is on the way!",
        ),
        attributes={"priority": "high"},
    )
    publish_event(event)
