from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from messaging_client import get_sqs_client, resolve_queue_url, sqs_message_attributes
from messaging_models import BatchPublishResult, envelopes_from_iterable


PROVIDER = "amazon_sqs"


def batch_publish(messages: Iterable[Dict[str, Any]], queue_url: Optional[str] = None) -> BatchPublishResult:
    client = get_sqs_client()
    destination = resolve_queue_url(queue_url)
    envelopes = envelopes_from_iterable(messages)
    entries = [
        {
            "Id": envelope.message_id,
            "MessageBody": envelope.to_json(),
            "MessageAttributes": sqs_message_attributes(envelope.attributes),
        }
        for envelope in envelopes
    ]
    response = client.send_message_batch(QueueUrl=destination, Entries=entries)
    successful_ids = [item["Id"] for item in response.get("Successful", [])]
    failed_ids = [item["Id"] for item in response.get("Failed", [])]
    return BatchPublishResult(
        provider=PROVIDER,
        destination=destination,
        successful_ids=successful_ids,
        failed_ids=failed_ids,
    )
