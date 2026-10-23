import json
from typing import List
from observability_models import LogEvent


def incident_summary(errors: List[LogEvent]) -> dict:
    """Summarizes error‑log findings for incident review.

    Produces a high‑level report containing:
        * total number of error events
        * distinct correlation IDs (requests) involved
        * earliest and latest timestamps
        * top 5 error messages by frequency
        * any unsafe content detections (via `log_text_safety` helper)

    Returns a dict that can be serialized as JSON for downstream incident management systems.
    """
    if not errors:
        return {"total_errors": 0, "correlation_ids": [], "summary": {}}

    # Basic aggregates
    timestamps = [evt["timestamp"] for evt in errors]
    corr_ids = {evt.get("correlation_id") for evt in errors}
    earliest = min(timestamps)
    latest = max(timestamps)
    total = len(errors)

    # Frequency of error messages
    freq = {}
    for evt in errors:
        msg = evt["message"]
        freq[msg] = freq.get(msg, 0) + 1
    top_messages = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]

    # Optional safety check (optional import; skipped if not present)
    try:
        from log_text_safety import contains_unsafe_content

        unsafe = [evt for evt in errors if contains_unsafe_content(evt["message"])]
    except Exception:
        unsafe = []

    return {
        "total_errors": total,
        "correlation_ids": list(corr_ids),
        "time_range": {"earliest": earliest, "latest": latest},
        "top_error_messages": top_messages,
        "unsafe_content_found": bool(unsafe),
    }
