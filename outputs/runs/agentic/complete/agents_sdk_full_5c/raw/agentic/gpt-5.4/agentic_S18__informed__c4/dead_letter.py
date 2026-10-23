from __future__ import annotations

from typing import Any, Dict, Optional

from messaging_client import get_sqs_client, resolve_dead_letter_queue_url, sqs_message_attributes
from messaging_models import MessageEnvelope, PublishResult, normalize_payload


PROVIDER = "amazon_sqs"


def send_to_dead_letter(payload: Dict[str, Any], dead_letter_queue_url: Optional[str] = None, reason: str = "processing_failed") -> PublishResult:
    client = get_sqs_client()
    destination = resolve_dead_letter_queue_url(dead_letter_queue_url)
    envelope = MessageEnvelope(
        body=normalize_payload(payload),
        attributes={"dead_letter_reason": reason},
    )
    response = client.send_message(
        QueueUrl=destination,
        MessageBody=envelope.to_json(),
        MessageAttributes=sqs_message_attributes(envelope.attributes),
    )
    return PublishResult(
        provider=PROVIDER,
        destination=destination,
        message_id=response["MessageId"],
        status="dead_lettered",
    )
