import json

from google.cloud import pubsub_v1

from messaging_client import get_subscriber, subscription_path
from messaging_models import ConsumeResponse, decode_json_message


def consume_event(subscription: str) -> ConsumeResponse:
    subscriber = get_subscriber()
    path = subscription_path(subscription)
    response = subscriber.pull(
        request={"subscription": path, "max_messages": 1}, timeout=10
    )
    if not response.received_messages:
        return ConsumeResponse(message_id=None, payload={})
    msg = response.received_messages[0]
    payload = decode_json_message(msg.message.data)
    msg.ack()
    return ConsumeResponse(
        message_id=msg.message.message_id,
        payload=payload,
        attributes=dict(msg.message.attributes),
    )


def main() -> None:
    result = consume_event("events-sub")
    print(json.dumps({"message_id": result.message_id, "payload": result.payload}))


if __name__ == "__main__":
    main()
