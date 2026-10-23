from __future__ import annotations

from typing import Any, Dict, Optional

from messaging_client import get_sqs_client, resolve_queue_url, sqs_message_attributes
from messaging_models import MessageEnvelope, PublishResult, normalize_payload


PROVIDER = "amazon_sqs"


def publish_event(payload: Dict[str, Any], queue_url: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None) -> PublishResult:
    client = get_sqs_client()
    destination = resolve_queue_url(queue_url)
    envelope = MessageEnvelope(body=normalize_payload(payload), attributes=attributes or {})
    response = client.send_message(
        QueueUrl=destination,
        MessageBody=envelope.to_json(),
        MessageAttributes=sqs_message_attributes(envelope.attributes),
    )
    return PublishResult(
        provider=PROVIDER,
        destination=destination,
        message_id=response["MessageId"],
        status="published",
    )
