from __future__ import annotations

from collections import Counter

from observability_models import IncidentSummary, LogQueryResponse


def summarize_error_logs(response: LogQueryResponse) -> IncidentSummary:
    services = Counter()
    for entry in response.entries:
        payload = entry.get("payload", {}) or {}
        service = payload.get("service") or payload.get("labels", {}).get("service")
        if service:
            services[service] += 1
    count = len(response.entries)
    details = f"Observed {count} error logs across {len(services)} services."
    return IncidentSummary(
        title="Incident review summary",
        details=details,
        affected_services=list(services.keys()),
        error_count=count,
    )
