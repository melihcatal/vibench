import os
import sys
from datetime import datetime, timezone, timedelta

from observability_models import LogQueryResult, SlsClientConfig, LogSeverity
from observability_client import (
    ObservabilityClient,
    build_error_query,
    build_time_range_query,
    extract_error_messages,
)


def query_error_logs(
    severity: str = "ERROR",
    hours_back: int = 1,
    service: str | None = None,
    max_results: int = 100,
) -> LogQueryResult:
    config = SlsClientConfig.from_env()
    client = ObservabilityClient(config)

    from_time, to_time = build_time_range_query(
        from_time=datetime.now(timezone.utc) - timedelta(hours=hours_back),
        to_time=datetime.now(timezone.utc),
    )

    query = build_error_query(severity=severity)
    if service:
        query = f"{query} and service: {service}"

    result = client.get_logs(
        query=query,
        from_time=from_time,
        to_time=to_time,
        line=max_results,
        reverse=True,
    )
    return result


def get_error_log_summaries(
    severity: str = "ERROR",
    hours_back: int = 1,
    service: str | None = None,
    max_results: int = 100,
) -> list[dict]:
    result = query_error_logs(
        severity=severity,
        hours_back=hours_back,
        service=service,
        max_results=max_results,
    )
    error_logs = extract_error_messages(result)
    summaries = []
    for log in error_logs:
        summaries.append(
            {
                "timestamp": log.get("timestamp", ""),
                "severity": log.get("severity", ""),
                "message": log.get("message", ""),
                "service": log.get("service", ""),
                "correlation_id": log.get("correlation_id", ""),
            }
        )
    return summaries


if __name__ == "__main__":
    severity = sys.argv[1] if len(sys.argv) > 1 else "ERROR"
    hours_back = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    service = sys.argv[3] if len(sys.argv) > 3 else None
    summaries = get_error_log_summaries(
        severity=severity, hours_back=hours_back, service=service
    )
    for s in summaries:
        print(s)
