from collections import Counter
from typing import List
from google.cloud import logging_v2
from observability_models import IncidentSummary, LogQueryResponse
from query_error_logs import query_error_logs


def incident_summary(hours: int = 24) -> IncidentSummary:
    response = query_error_logs(hours=hours, severity="ERROR", limit=100)
    messages = [record.message for record in response.records]
    counts = Counter(messages)
    top_messages = [message for message, _ in counts.most_common(5)]
    earliest = min((record.timestamp for record in response.records), default=None)
    latest = max((record.timestamp for record in response.records), default=None)
    return IncidentSummary(title="Error log incident summary", summary=f"Found {len(response.records)} error log entries in the last {hours} hours.", error_count=len(response.records), earliest_timestamp=earliest, latest_timestamp=latest, top_messages=top_messages)
