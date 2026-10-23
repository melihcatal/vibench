import json

# [LATER-STEP] message_summary.py
# Summarize results of message processing (counts, errors, timestamps)

import datetime


class MessageSummary:
    """Aggregated summary of a batch of message operations."""

    def __init__(
        self,
        processed: int = 0,
        failed: int = 0,
        errors: list[str] = None,
        completed_at: datetime.datetime = None,
    ):
        self.processed = processed
        self.failed = failed
        self.errors = errors or []
        self.completed_at = completed_at or datetime.datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "processed": self.processed,
            "failed": self.failed,
            "errors": self.errors,
            "completed_at": self.completed_at.isoformat() + "Z",
        }

    def increment_processed(self):
        self.processed += 1

    def increment_failed(self, error_msg: str):
        self.failed += 1
        self.errors.append(error_msg)
