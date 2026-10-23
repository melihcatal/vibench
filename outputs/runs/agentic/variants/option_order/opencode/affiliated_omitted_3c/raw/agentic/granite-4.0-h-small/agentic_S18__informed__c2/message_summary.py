from typing import List, TypedDict

from messaging_models import BatchPublishResponse, ConsumeResponse, DeadLetterRequest


class MessageSummary(TypedDict):
    processed_count: int
    failed_count: int
    dead_lettered: List[DeadLetterRequest]


def summarize_processing(
    batches: List[BatchPublishResponse],
    consumed: List[ConsumeResponse],
    dead_lettered: List[DeadLetterRequest],
) -> MessageSummary:
    """Aggregate results from publish/consume/dead-letter operations into a concise summary."""
    total_processed = sum(b["sent_count"] for b in batches)
    total_failed = sum(b["failed_count"] for b in batches)
    return {
        "processed_count": total_processed,
        "failed_count": total_failed,
        "dead_lettered": dead_lettered,
    }
