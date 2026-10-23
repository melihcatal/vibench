from __future__ import annotations

from observability_client import build_log_event, get_client


def write_correlated_logs(correlation_id: str, messages: list[str], severity: str = "INFO"):
    client = get_client()
    results = []
    for index, message in enumerate(messages):
        event = build_log_event(
            message=message,
            severity=severity,
            correlation_id=correlation_id,
            sequence=index,
            scenario="correlated-request",
        )
        results.append(client.write_log(event))
    return results
