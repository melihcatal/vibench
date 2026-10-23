import json
from google.cloud import pubsub_v1

from messaging_client import load_config, publisher, topic_path
from messaging_models import EventRequest, EventResponse, normalize_attributes


def publish_event(event: EventRequest) -> EventResponse:
    cfg = load_config()
    topic = topic_path(cfg.publish_topic)
    client = publisher()
    data = event.to_json().encode("utf-8")
    future = client.publish(topic, data=data, **normalize_attributes(event.attributes))
    message_id = future.result()
    return EventResponse(message_id=message_id)


if __name__ == "__main__":
    sample = EventRequest(event_id="evt-001", payload={"type": "order.created", "amount": 42.5}, attributes={"source": "checkout"})
    result = publish_event(sample)
    print(json.dumps({"message_id": result.message_id, "acknowledged": result.acknowledged}))
