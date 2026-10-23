from __future__ import annotations

import os

from messaging_client import build_sns_client, load_config, publish_json
from messaging_models import MessageEnvelope, PublishRequest, coerce_message_payload


def publish_event(payload: object) -> dict:
    config = load_config()
    client = build_sns_client(config)
    envelope = MessageEnvelope(
        message_id=os.getenv("MESSAGE_ID", "event-1"),
        payload=coerce_message_payload(payload),
        attributes={"scenario": "publish_event", "provider": "aws-sns"},
    )
    request = PublishRequest(topic_name=config.topic_arn, envelope=envelope)
    return publish_json(client, request)
