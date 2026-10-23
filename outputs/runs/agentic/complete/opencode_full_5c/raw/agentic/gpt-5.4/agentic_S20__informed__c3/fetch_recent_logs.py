from __future__ import annotations

from typing import Any, Dict, List, Optional

from observability_client import (
    DatadogObservabilityClient,
    build_field_query,
    iso_utc_minutes_ago,
    iso_utc_now,
)
from observability_models import LogQuery, NormalizedLogEntry


def fetch_recent_logs(
    field_filters: Optional[Dict[str, Any]] = None,
    lookback_minutes: int = 30,
    limit: int = 100,
) -> List[NormalizedLogEntry]:
    client = DatadogObservabilityClient()
    query = build_field_query(field_filters)
    return client.search_logs(
        LogQuery(
            start_time=iso_utc_minutes_ago(lookback_minutes),
            end_time=iso_utc_now(),
            query=query,
            limit=limit,
        )
    )
