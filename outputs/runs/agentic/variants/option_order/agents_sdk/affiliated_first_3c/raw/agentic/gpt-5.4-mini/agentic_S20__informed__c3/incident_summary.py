from __future__ import annotations

from collections import Counter

from observability_models import IncidentSummary, QueryResponse


def incident_summary(results: QueryResponse) -> dict:
    severities = Counter(item.get("severity", "UNKNOWN") for item in results.records)
    correlation_ids = sorted({item.get("correlation_id") for item in results.records if item.get("correlation_id")})
    findings = [f"{count} log entries by severity {severity}" for severity, count in sorted(severities.items(), key=lambda x: x[0], reverse=True)]
    return IncidentSummary(
        title="Log incident review",
        severity=severities.most_common(1)[0][0] if severities else "UNKNOWN",
        findings=findings,
        affected_correlation_ids=correlation_ids,
        suggested_next_steps=["Investigate correlated traces", "Check recent deployments", "Escalate if impact is customer-facing"],
    ).to_dict()
