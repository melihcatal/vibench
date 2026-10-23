from __future__ import annotations

from messaging_models import MessageSummary


def summarize_message_processing(total: int, success: int, failed: int) -> MessageSummary:
    return MessageSummary(total=total, success=success, failed=failed, note="pubsub-processing-summary")
