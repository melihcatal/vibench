from query_error_logs import query_error_logs
import json


def incident_summary(error_threshold: int = 10, time_window_hours: int = 24) -> dict:
    """Summarizes error‑log findings for incident review.

    Queries recent errors, counts them, extracts top error messages,
    and returns a concise incident report.

    Args:
        error_threshold (int): Treats any error count above this as an incident.
        time_window_hours (int): Lookback period for the query.

    Returns:
        dict: Summary containing total count and a sample of top errors.
    """
    logs = query_error_logs(severity="error", start_time=f"{time_window_hours}h")
    total = len(logs)
    summary = {
        "incident": total >= error_threshold,
        "total_errors": total,
        "sample_errors": [json.loads(l["text"]) for l in logs[:5]],
    }
    return summary
