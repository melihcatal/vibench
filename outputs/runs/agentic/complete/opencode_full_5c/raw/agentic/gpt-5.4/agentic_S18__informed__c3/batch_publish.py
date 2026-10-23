from __future__ import annotations

from typing import Iterable, List

from messaging_client import batch_entries, get_queue_url, sqs_client
from messaging_models import BatchPublishItem


def batch_publish(
    items: Iterable[BatchPublishItem], queue_url: str | None = None
) -> dict:
    client = sqs_client()
    destination = queue_url or get_queue_url("AWS_SQS_QUEUE_URL")
    entries = batch_entries(items)
    response = client.send_message_batch(QueueUrl=destination, Entries=entries)
    return {
        "queue_url": destination,
        "successful": response.get("Successful", []),
        "failed": response.get("Failed", []),
    }
