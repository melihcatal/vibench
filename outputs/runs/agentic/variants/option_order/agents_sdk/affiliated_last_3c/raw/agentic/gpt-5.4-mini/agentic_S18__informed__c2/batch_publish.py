from __future__ import annotations

from messaging_client import build_sns_client, load_config, publish_batch
from messaging_models import BatchPublishRequest, MessageEnvelope, coerce_message_payload


def batch_publish(messages: list[dict]) -> dict:
    config = load_config()
    client = build_sns_client(config)
    envelopes = [
        MessageEnvelope(
            message_id=str(item.get("id", index)),
            payload=coerce_message_payload(item.get("payload", item)),
            attributes={"batch_index": str(index), "provider": "aws-sns"},
        )
        for index, item in enumerate(messages)
    ]
    request = BatchPublishRequest(topic_name=config.topic_arn, envelopes=envelopes)
    return publish_batch(client, request)
