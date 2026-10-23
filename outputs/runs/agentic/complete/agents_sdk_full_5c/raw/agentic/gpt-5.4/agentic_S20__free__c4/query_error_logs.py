from __future__ import annotations

from typing import List

from observability_client import DatadogObservabilityClient, default_time_range
from observability_models import NormalizedLogRecord, normalize_datadog_log


def query_error_logs(service: str, minutes: int = 30, limit: int = 100) -> List[NormalizedLogRecord]:
    client = DatadogObservabilityClient()
    window = default_time_range(minutes)
    query = f'service:{service} @severity:(ERROR OR CRITICAL OR ALERT OR EMERGENCY)'
    results = client.list_logs(query=query, start=window["start"], end=window["end"], limit=limit)
    return [normalize_datadog_log(item) for item in results]
