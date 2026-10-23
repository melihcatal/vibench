from google.cloud.pubsub_v1 import SubscriberClient
from google.cloud.pubsub_v1.types import PullRequest, ReceivedMessage

from messaging_client import (
    create_subscriber_client,
    get_subscription_path,
    extract_message_text,
    extract_message_attributes,
    acknowledge_message,
)
from messaging_models import PubSubEvent, ConsumeResult


def consume_event(
    max_messages: int = 1,
    auto_acknowledge: bool = True,
) -> ConsumeResult:
    subscriber: SubscriberClient = create_subscriber_client()
    subscription_path = get_subscription_path()

    pull_request = PullRequest(
        subscription=subscription_path,
        max_messages=max_messages,
        return_immediately=True,
    )
    response = subscriber.pull(request=pull_request)

    if not response.received_messages:
        return ConsumeResult(event=None, status="no_messages")

    received: ReceivedMessage = response.received_messages[0]
    ack_id = received.ack_id
    message = received.message

    text = extract_message_text(message)
    attributes = extract_message_attributes(message)

    event = PubSubEvent(
        event_id=attributes.get("event_id", ""),
        event_type=attributes.get("event_type", "default"),
        source=attributes.get("source", "unknown"),
        timestamp=attributes.get("timestamp", ""),
        payload={},
        attributes=attributes,
    )

    from messaging_models import normalize_payload

    event.payload = normalize_payload(text)

    if auto_acknowledge and ack_id:
        acknowledge_message(subscriber, subscription_path, ack_id)

    return ConsumeResult(
        event=event,
        ack_id=ack_id,
        status="consumed",
    )


if __name__ == "__main__":
    import json

    result = consume_event()
    print(json.dumps(result.to_dict(), indent=2))
