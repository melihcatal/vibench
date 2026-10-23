from typing import List, Dict
from query_error_logs import query_error_logs
from datadog_api_client.v2.model.log import Log


def summarize_error_logs_for_incident(hours: int = 1) -> Dict[str, Any]:
    """
    Summarizes error log findings from Datadog for incident review.

    Args:
        hours: Time range in hours to query error logs from.

    Returns:
        Dictionary containing a summary of error logs, including counts, sample messages,
        and common patterns.
    """
    error_logs = query_error_logs(severity="ERROR", hours=hours)

    if not error_logs:
        return {"summary": "No error logs found in the specified time range."}

    error_messages = [log.get("message", "No message") for log in error_logs]
    unique_errors = list(set(error_messages))

    return {
        "total_errors": len(error_logs),
        "unique_error_count": len(unique_errors),
        "sample_messages": unique_errors[:5],
        "common_patterns": _identify_common_patterns(error_messages),
    }


def _identify_common_patterns(messages: List[str]) -> List[Dict[str, Any]]:
    """
    Identifies common patterns in error messages.

    Args:
        messages: List of error messages.

    Returns:
        List of dictionaries containing pattern and count.
    """
    pattern_counts = {}
    for message in messages:
        if "timeout" in message.lower():
            pattern_counts["timeout"] = pattern_counts.get("timeout", 0) + 1
        elif "connection refused" in message.lower():
            pattern_counts["connection_refused"] = (
                pattern_counts.get("connection_refused", 0) + 1
            )
        elif "null pointer" in message.lower():
            pattern_counts["null_pointer"] = pattern_counts.get("null_pointer", 0) + 1
        elif "404" in message:
            pattern_counts["not_found"] = pattern_counts.get("not_found", 0) + 1
        else:
            pattern_counts["other"] = pattern_counts.get("other", 0) + 1

    return [
        {"pattern": pattern, "count": count}
        for pattern, count in pattern_counts.items()
    ]
