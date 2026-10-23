import json
from google.cloud import pubsub_v1

from messaging_client import load_config, subscriber, subscription_path
from messaging_models import MessageRecord, parse_json_payload


def consume_one_message(timeout: float = 5.0) -> MessageRecord | None:
    cfg = load_config()
    sub = subscription_path(cfg.consume_subscription)
    client = subscriber()
    response = client.pull(subscription=sub, max_messages=1, timeout=timeout)
    if not response.received_messages:
        return None
    received = response.received_messages[0]
    payload = parse_json_payload(received.message.data)
    client.acknowledge(subscription=sub, ack_ids=[received.ack_id])
    return MessageRecord(
        message_id=received.message.message_id,
        status="consumed",
        body=json.dumps(payload),
        attributes=dict(received.message.attributes),
    )


if __name__ == "__main__":
    record = consume_one_message()
    print(None if record is None else record.body)
