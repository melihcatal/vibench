from __future__ import annotations

from typing import Any, Mapping, Optional
import json

from messaging_client import get_sqs_client, get_dead_letter_queue_url
from messaging_models import PublishResult, build_envelope


PROVIDER = "aws-sqs-dlq"


def send_to_dead_letter(failed_payload: Mapping[str, Any] | str, reason: str, original_message_id: Optional[str] = None, dead_letter_queue_url: Optional[str] = None) -> PublishResult:
    client = get_sqs_client()
    queue_url = get_dead_letter_queue_url(dead_letter_queue_url)
    envelope = build_envelope(
        event_type="dead_letter",
        payload={
            "reason": reason,
            "original_message_id": original_message_id,
            "failed_payload": failed_payload if isinstance(failed_payload, Mapping) else json.loads(failed_payload),
        },
        attributes={"failure_reason": reason},
        message_id=original_message_id,
    )
    response = client.send_message(
        QueueUrl=queue_url,
        MessageBody=envelope.to_json(),
        MessageAttributes={
            "failure_reason": {"DataType": "String", "StringValue": reason}
        },
    )
    return PublishResult(
        provider=PROVIDER,
        destination=queue_url,
        message_id=response["MessageId"],
        status="dead_lettered",
    )
