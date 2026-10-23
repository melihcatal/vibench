import json
from messaging_client import (
    load_config,
    get_subscriber_client,
    build_subscription_path,
    pull_one_message,
    acknowledge_message,
    parse_received_message,
)
from messaging_models import ConsumeResult


def consume_event(auto_ack: bool = True) -> ConsumeResult:
    config = load_config()
    subscriber = get_subscriber_client()
    subscription_path = build_subscription_path(config)

    received = pull_one_message(subscriber, subscription_path, max_messages=1)

    if not received:
        return ConsumeResult(status="no_messages")

    received_msg = received[0]
    event = parse_received_message(received_msg)
    ack_id = received_msg.ack_id
    delivery_attempt = received_msg.delivery_attempt

    if auto_ack:
        acknowledge_message(subscriber, subscription_path, ack_id)

    return ConsumeResult(
        event=event,
        ack_id=ack_id,
        delivery_attempt=delivery_attempt,
        status="consumed",
    )


if __name__ == "__main__":
    result = consume_event(auto_ack=True)
    print(json.dumps(result.to_dict(), indent=2))
