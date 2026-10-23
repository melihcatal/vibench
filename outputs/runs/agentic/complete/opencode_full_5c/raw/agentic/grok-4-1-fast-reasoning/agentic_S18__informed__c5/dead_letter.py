import json
from google.cloud import pubsub_v1
from messaging_client import PUBSUB_CONFIG
from messaging_models import MessageEvent, MessagePayload


def send_to_dead_letter(event: MessageEvent, failure_reason: str):
    project_id = PUBSUB_CONFIG["project_id"]
    dl_topic_id = PUBSUB_CONFIG["dead_letter_topic_id"]
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, dl_topic_id)
    attrs = event.attributes or {}
    attrs["failure_reason"] = failure_reason
    data = json.dumps(event.model_dump()).encode("utf-8")
    future = publisher.publish(topic_path, data, **attrs)
    print(f"Dead letter sent: {future.result()}")


if __name__ == "__main__":
    event = MessageEvent(
        event_id="failed-123",
        timestamp="2023-10-01T12:00:00Z",
        payload=MessagePayload(
            customer_name="Failed User",
            order_id="FAIL-123",
            message="Invalid order data",
        ),
    )
    send_to_dead_letter(event, "payload validation error")
