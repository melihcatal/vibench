# message_summary.py
"""
Later-step scored implementation: message_summary.py
Summarizes Pub/Sub message processing results.
"""

from typing import List
from messaging_models import PubSubResult


def summarize_results(results: List[PubSubResult]) -> str:
    """Generate a concise summary of processing outcomes.

    Args:
        results (List[PubSubResult]): Collected results from publishing or consumption.

    Returns:
        str: A human-readable summary.
    """
    success = sum(1 for r in results if r.message_id)
    failed = sum(1 for r in results if r.error)
    total = len(results)
    return f"Processed {total} messages: {success} succeeded, {failed} failed."
