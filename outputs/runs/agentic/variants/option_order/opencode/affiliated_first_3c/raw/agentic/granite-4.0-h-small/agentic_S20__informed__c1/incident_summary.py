import os
from observability_models import LogEvent, denormalize_response
from observability_client import get_logging_client
import datetime


def incident_summary(error_logs):
    """Summarize error logs for incident review.

    Args:
        error_logs (list[dict]): Raw log entries.
    """
    # Normalize logs
    normalized = [denormalize_response(log) for log in error_logs]
    summary = {
        "total_errors": len(normalized),
        "earliest": min(log["timestamp"] for log in normalized) if normalized else None,
        "latest": max(log["timestamp"] for log in normalized) if normalized else None,
        "request_counts": {},
    }
    for log in normalized:
        req = log.get("correlation_id")
        summary["request_counts"][req] = summary["request_counts"].get(req, 0) + 1
    return summary
