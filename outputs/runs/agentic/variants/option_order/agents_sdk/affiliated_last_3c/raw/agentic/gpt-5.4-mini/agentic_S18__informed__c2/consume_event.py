from __future__ import annotations

from messaging_client import build_sqs_client, load_config, receive_one


def consume_event() -> dict:
    config = load_config()
    client = build_sqs_client(config)
    response = receive_one(client, config.queue_url)
    return response.__dict__ if response else {"message_id": "", "payload": {}, "attributes": {}, "ack_id": None}
