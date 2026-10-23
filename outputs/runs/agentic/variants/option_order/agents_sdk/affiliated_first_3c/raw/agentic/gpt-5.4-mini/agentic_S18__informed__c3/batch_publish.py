from __future__ import annotations

from typing import Iterable, Mapping, Any

from messaging_client import publish_batch
from messaging_models import BatchPublishRequest, MessageEnvelope, normalize_attributes


def publish_messages(topic: str, messages: Iterable[Mapping[str, Any]]) -> list[str]:
    envelopes = []
    for message in messages:
        envelopes.append(
            MessageEnvelope(
                message_id=str(message.get("id", "")),
                payload=message.get("payload"),
                attributes=normalize_attributes(message.get("attributes")),
            )
        )
    return publish_batch(BatchPublishRequest(topic=topic, messages=envelopes))
