from __future__ import annotations

from typing import Dict, List

from observability_client import DatadogObservabilityClient, default_time_range
from observability_models import NormalizedLogRecord, normalize_datadog_log


def fetch_recent_logs(service: str, field_filters: Dict[str, str], minutes: int = 15, limit: int = 50) -> List[NormalizedLogRecord]:
    client = DatadogObservabilityClient()
    window = default_time_range(minutes)
    query_parts = [f"service:{service}"]
    for field_name, value in field_filters.items():
        query_parts.append(f"@{field_name}:{value}")
    query = " ".join(query_parts)
    results = client.list_logs(query=query, start=window["start"], end=window["end"], limit=limit)
    return [normalize_datadog_log(item) for item in results]
