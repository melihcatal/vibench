import json
from google.cloud import pubsub_v1

from messaging_client import load_config, publisher, topic_path
from messaging_models import EventRequest, batch_payloads, normalize_attributes


def batch_publish(events: list[EventRequest]) -> list[str]:
    cfg = load_config()
    topic = topic_path(cfg.publish_topic)
    client = publisher()
    payloads = batch_payloads(events)
    message_ids: list[str] = []
    for event, payload in zip(events, payloads):
        future = client.publish(topic, data=payload, **normalize_attributes(event.attributes))
        message_ids.append(future.result())
    return message_ids


if __name__ == "__main__":
    events = [
        EventRequest(event_id="evt-001", payload={"type": "order.created"}, attributes={"batch": "a"}),
        EventRequest(event_id="evt-002", payload={"type": "order.updated"}, attributes={"batch": "a"}),
    ]
    print(json.dumps({"message_ids": batch_publish(events)}))
