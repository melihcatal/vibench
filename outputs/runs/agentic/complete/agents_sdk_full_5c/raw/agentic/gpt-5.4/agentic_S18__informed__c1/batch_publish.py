from __future__ import annotations

from typing import Any, Iterable, Mapping, Optional

from messaging_client import get_sqs_client, get_sqs_queue_url
from messaging_models import build_envelope


PROVIDER = "aws-sqs"


def batch_publish(messages: Iterable[Mapping[str, Any]], queue_url: Optional[str] = None) -> dict:
    client = get_sqs_client()
    resolved_queue_url = get_sqs_queue_url(queue_url)
    entries = []
    for index, item in enumerate(messages):
        envelope = build_envelope(
            event_type=item["event_type"],
            payload=item["payload"],
            attributes=item.get("attributes", {}),
            message_id=item.get("message_id"),
        )
        entries.append(
            {
                "Id": envelope.message_id,
                "MessageBody": envelope.to_json(),
                "MessageAttributes": {
                    **{
                        key: {"DataType": "String", "StringValue": value}
                        for key, value in envelope.attributes.items()
                    },
                    "event_type": {"DataType": "String", "StringValue": envelope.event_type},
                },
            }
        )
        if index >= 9:
            break
    response = client.send_message_batch(QueueUrl=resolved_queue_url, Entries=entries)
    return {
        "provider": PROVIDER,
        "queue_url": resolved_queue_url,
        "successful": response.get("Successful", []),
        "failed": response.get("Failed", []),
    }
