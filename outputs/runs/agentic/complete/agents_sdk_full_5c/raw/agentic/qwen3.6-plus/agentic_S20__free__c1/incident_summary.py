"""
[LATER-STEP] incident_summary.py

Summarizes error-log findings for incident review using Datadog Managed Logs.
Queries Datadog for error logs, aggregates findings by service and correlation ID,
and produces a structured incident summary report.

Uses datadog_api_client SDK targeting the Datadog API provider.
"""

import json
import sys
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from typing import Dict, Any, List

from datadog_api_client import ApiClient
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_filter import LogsListRequestFilter
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_list_request_sort import LogsListRequestSort

from observability_client import get_logs_client, format_datadog_timestamp
from observability_models import normalize_datadog_log_response, IncidentSummary


def build_incident_summary(
    incident_id: str,
    service: str | None = None,
    env: str = "production",
    hours: int = 2,
    limit: int = 500,
) -> Dict[str, Any]:
    """
    Build an incident summary by querying Datadog for recent error logs.

    Aggregates errors by service, extracts unique correlation IDs,
    collects distinct error messages, and determines the time range
    of the incident for review.

    Args:
        incident_id: Unique identifier for the incident report.
        service: Optional specific service to scope the incident.
        env: Deployment environment.
        hours: Hours of historical error logs to include.
        limit: Maximum error log entries to analyze.

    Returns:
        Dict with the IncidentSummary report.
    """
    now = datetime.now(timezone.utc)
    from_time = now - timedelta(hours=hours)

    from_ts = format_datadog_timestamp(from_time.isoformat())
    to_ts = format_datadog_timestamp(now.isoformat())

    query_parts = [f"env:{env}", "status:(error OR critical)"]
    if service:
        query_parts.append(f"service:{service}")
    full_query = " ".join(query_parts)

    try:
        logs_api: LogsApi = get_logs_client()

        log_filter = LogsListRequestFilter(
            query=full_query,
            _from=from_ts,
            to=to_ts,
        )
        request = LogsListRequest(
            filter=log_filter,
            page=LogsListRequestPage(limit=limit),
            sort=LogsListRequestSort("-timestamp"),
        )

        with ApiClient() as api_client:
            api_logs_api = LogsApi(api_client)
            response = api_logs_api.list_logs(body=request)

        response_data = response.to_dict() if hasattr(response, "to_dict") else response
        entries = normalize_datadog_log_response(response_data)

        services = []
        error_messages = []
        correlation_ids = []
        error_counts_by_service = defaultdict(int)

        for entry in entries:
            services.append(entry.service)
            error_messages.append(entry.message)
            error_counts_by_service[entry.service] += 1
            if entry.correlation_id:
                correlation_ids.append(entry.correlation_id)

        summary = IncidentSummary(
            incident_id=incident_id,
            total_errors=len(entries),
            affected_services=list(error_counts_by_service.keys()),
            error_messages=error_messages[:20],
            time_range={
                "from": from_time.isoformat(),
                "to": now.isoformat(),
            },
            correlation_ids=correlation_ids,
        )

        report = summary.to_report()
        report["error_counts_by_service"] = dict(error_counts_by_service)
        report["analysis_note"] = f"Analyzed {len(entries)} error entries from Datadog for incident {incident_id}"

        return report

    except Exception as exc:
        return {
            "status": "error",
            "incident_id": incident_id,
            "message": f"Failed to build incident summary from Datadog: {exc}",
        }


def main() -> None:
    """CLI entry point for generating an incident summary from Datadog logs."""
    if len(sys.argv) < 2:
        print("Usage: incident_summary.py <incident_id> [service] [env] [hours]")
        sys.exit(1)

    incident_id = sys.argv[1]
    service = sys.argv[2] if len(sys.argv) > 2 else None
    env = sys.argv[3] if len(sys.argv) > 3 else "production"
    hours = int(sys.argv[4]) if len(sys.argv) > 4 else 2

    result = build_incident_summary(incident_id, service, env, hours)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
