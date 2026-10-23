from collections import Counter
from observability_models import IncidentSummary, LogQueryResult


def summarize(result: LogQueryResult) -> IncidentSummary:
    messages = [item.get("message", "") for item in result.items if isinstance(item, dict)]
    correlation_ids = [item.get("correlation_id", "") for item in result.items if isinstance(item, dict) and item.get("correlation_id")]
    severity = "high" if result.total > 10 else "medium" if result.total > 0 else "low"
    return IncidentSummary(
        severity=severity,
        time_window="recent",
        error_count=result.total,
        correlation_ids=list(Counter(correlation_ids).keys()),
        messages=messages[:10],
    )
