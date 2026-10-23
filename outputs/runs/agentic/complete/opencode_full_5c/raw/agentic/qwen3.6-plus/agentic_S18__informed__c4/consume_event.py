from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client, subscription_path, load_topic_config
from messaging_models import PubSubEvent, ConsumeResult


def consume_event(
    subscription_name: str | None = None, ack_timeout: float = 30.0
) -> ConsumeResult:
    config = load_topic_config()
    project_id = config["project_id"]
    sub = subscription_name or config["subscription_name"]
    sub_path = subscription_path(project_id, sub)
    subscriber = get_subscriber_client()

    response = subscriber.pull(
        request={"subscription": sub_path, "max_messages": 1},
        timeout=ack_timeout,
    )

    if not response.received_messages:
        return ConsumeResult(message_id="", acknowledged=False)

    received = response.received_messages[0]
    message = received.message
    raw_data = message.data.decode("utf-8")

    try:
        event = PubSubEvent.from_json(raw_data)
    except Exception:
        event = None

    subscriber.acknowledge(
        request={"subscription": sub_path, "ack_ids": [received.ack_id]}
    )

    return ConsumeResult(
        message_id=message.message_id,
        event=event,
        raw_data=raw_data if event is None else None,
        delivery_attempt=received.delivery_attempt,
        acknowledged=True,
    )


if __name__ == "__main__":
    result = consume_event()
    print(result.to_event().to_json() if result.event else "No message received")
