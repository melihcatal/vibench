from messaging_models import MessageRecord
from typing import List


def summarize_records(records: List[MessageRecord]) -> dict:
    """Create a concise summary of message processing results."""
    summary = {
        "total": len(records),
        "success": 0,
        "dead_lettered": 0,
        "failed": 0,
        "details": [],
    }
    for rec in records:
        if rec.status == "processed":
            summary["success"] += 1
        elif rec.status == "dead_lettered":
            summary["dead_lettered"] += 1
        else:
            summary["failed"] += 1
        summary["details"].append(
            {
                "status": rec.status,
                "error": rec.error,
                "payload": rec.processed if rec.processed else rec.original,
            }
        )
    return summary
