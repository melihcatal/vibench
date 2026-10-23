"""
[LATER-STEP] Summarizes error-log findings for incident review.

Uses the Datadog v2 Logs Search API to retrieve recent error logs, then
aggregates and summarizes findings for post-incident review.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from observability_models import (
    LogQueryResponse,
    format_time_window,
    severity_filter,
)
from observability_client import execute_log_query


def _query_error_logs(
    severity: str = "error",
    minutes_ago: int = 60,
    service: Optional[str] = None,
    limit: int = 200,
) -> LogQueryResponse:
    """Internal helper to query error logs from Datadog."""
    time_from, time_to = format_time_window(minutes_ago)
    severity_query = severity_filter(severity)

    filters = [severity_query]
    if service:
        filters.append(f"service:{service}")

    query = " AND ".join(filters)

    raw = execute_log_query(
        query=query,
        time_from=time_from.isoformat(),
        time_to=time_to.isoformat(),
        limit=limit,
        sort="-timestamp",
    )
    return LogQueryResponse.from_datadog_response(raw)


def summarize_errors(
    service: Optional[str] = None,
    minutes_ago: int = 60,
    top_n: int = 10,
) -> Dict[str, Any]:
    """
    Retrieve and summarize error logs for incident review.

    Aggregates errors by service, status, and message patterns to produce
    a concise incident summary report.

    Args:
        service: Optional service name to scope the review.
        minutes_ago: Time window to look back.
        top_n: Number of top error patterns to include.

    Returns:
        Summary dictionary with counts, top errors, and timeline data.
    """
    response = _query_error_logs(
        severity="error",
        minutes_ago=minutes_ago,
        service=service,
        limit=500,
    )

    if not response.entries:
        return {
            "review_window_minutes": minutes_ago,
            "total_errors": 0,
            "summary": "No error logs found in the specified time window.",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    # Aggregate by status
    status_counts = Counter(e.status for e in response.entries)

    # Aggregate by service
    service_counts = Counter(e.service for e in response.entries)

    # Aggregate by correlation ID to find affected requests
    affected_correlations = set()
    for e in response.entries:
        if e.correlation_id:
            affected_correlations.add(e.correlation_id)

    # Group error messages and find top patterns
    message_counter: Counter = Counter()
    for e in response.entries:
        message_counter[e.message] += 1

    top_errors = [
        {"message": msg, "count": count}
        for msg, count in message_counter.most_common(top_n)
    ]

    # Build timeline bucketing (errors per 5-minute interval)
    time_buckets: Dict[str, int] = defaultdict(int)
    for e in response.entries:
        bucket_key = e.timestamp.strftime("%Y-%m-%dT%H:%M")
        time_buckets[bucket_key] += 1

    timeline = dict(sorted(time_buckets.items()))

    # Collect unique error messages for detail
    unique_messages = list(set(e.message for e in response.entries))[:20]

    summary = {
        "review_window_minutes": minutes_ago,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_errors_found": response.total_count,
        "errors_returned": len(response.entries),
        "affected_services": dict(service_counts),
        "severity_breakdown": dict(status_counts),
        "affected_request_count": len(affected_correlations),
        "top_error_patterns": top_errors,
        "error_timeline": timeline,
        "sample_messages": unique_messages,
    }

    return summary


def generate_incident_report(
    summary: Dict[str, Any],
    incident_id: Optional[str] = None,
) -> str:
    """
    Generate a human-readable incident report from the error summary.
    """
    lines = [
        "=" * 60,
        "INCIDENT REVIEW SUMMARY",
        "=" * 60,
    ]

    if incident_id:
        lines.append(f"Incident ID: {incident_id}")

    lines.append(f"Generated at: {summary.get('generated_at', 'N/A')}")
    lines.append(f"Review window: {summary.get('review_window_minutes', 'N/A')} minutes")
    lines.append(f"Total errors found: {summary.get('total_errors_found', 0)}")
    lines.append("")

    affected_services = summary.get("affected_services", {})
    if affected_services:
        lines.append("Affected Services:")
        for svc, count in sorted(affected_services.items(), key=lambda x: -x[1]):
            lines.append(f"  - {svc}: {count} errors")
        lines.append("")

    top_errors = summary.get("top_error_patterns", [])
    if top_errors:
        lines.append(f"Top Error Patterns (up to 10):")
        for i, err in enumerate(top_errors, 1):
            lines.append(f"  {i}. [{err['count']}x] {err['message'][:120]}")
        lines.append("")

    affected_count = summary.get("affected_request_count", 0)
    lines.append(f"Unique affected requests: {affected_count}")
    lines.append("")

    timeline = summary.get("error_timeline", {})
    if timeline:
        lines.append("Error Timeline:")
        for ts, count in list(timeline.items())[-10:]:
            bar = "#" * min(count, 40)
            lines.append(f"  {ts} | {bar} ({count})")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def main() -> None:
    """Example: generate an incident error summary."""
    summary = summarize_errors(
        service="api-gateway",
        minutes_ago=30,
        top_n=5,
    )

    report = generate_incident_report(summary, incident_id="INC-2024-001")
    print(report)

    print("\nJSON Summary:")
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
