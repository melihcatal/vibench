from collections import Counter

from observability_client import query_recent_logs
from observability_models import IncidentSummary


def summarize_incident(start_time: str, end_time: str) -> IncidentSummary:
    response = query_recent_logs(start_time, end_time, filters={"severity": "ERROR"}, limit=100)
    severities = Counter(record.get("severity", "ERROR") for record in response.records)
    summary = f"Found {len(response.records)} error log entries in the selected time range."
    return IncidentSummary(title="Error log review", summary=summary, error_count=len(response.records), severity_breakdown=dict(severities))


if __name__ == "__main__":
    summarize_incident("0", "0")
