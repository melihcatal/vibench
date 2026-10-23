from __future__ import annotations

from typing import Any, Dict, List

from observability_client import list_logs
from observability_models import (
    RetrievedLog,
    normalize_datadog_log_item,
    normalize_timestamp,
)


def query_error_logs(
    *,
    service: str,
    severity: str,
    start_time: str,
    end_time: str,
    limit: int = 100,
) -> List[RetrievedLog]:
    query = f"service:{service} status:{severity.lower()}"
    response = list_logs(
        query=query,
        start=normalize_timestamp(start_time),
        end=normalize_timestamp(end_time),
        limit=limit,
    )
    return [normalize_datadog_log_item(item.to_dict()) for item in response.data]
