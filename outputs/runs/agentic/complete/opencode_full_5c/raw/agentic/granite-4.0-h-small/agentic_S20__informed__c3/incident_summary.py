import os
from query_error_logs import query_error_logs
from datetime import datetime, timedelta


def incident_summary(
    start_time: datetime, end_time: datetime, severity_threshold: str = "ERROR"
):
    """Summarize error‑log findings for incident review.
    Returns a concise report with counts and representative samples.
    """
    errors = query_error_logs(start_time, end_time, severity_threshold)
    count = len(errors)
    samples = errors[:5]  # first few samples for context
    summary = {
        "total_error_count": count,
        "sample_logs": samples,
        "time_range": {"start": start_time.isoformat(), "end": end_time.isoformat()},
    }
    return summary
