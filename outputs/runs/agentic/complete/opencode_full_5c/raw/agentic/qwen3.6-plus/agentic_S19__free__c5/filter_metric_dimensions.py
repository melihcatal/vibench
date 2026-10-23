from datetime import datetime
from typing import Dict, List, Optional

import requests

from observability_client import (
    DATADOG_API_BASE,
    create_datadog_session,
    validate_datadog_credentials,
)
from observability_models import (
    MetricDataPoint,
    MetricFilter,
    normalize_datadog_response,
)


def filter_metric_dimensions(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimension_filters: Dict[str, List[str]],
    aggregation: str = "avg",
    interval: int = 60,
) -> List[MetricDataPoint]:
    if not validate_datadog_credentials():
        raise ValueError(
            "Datadog credentials not configured. Set DATADOG_API_KEY and DATADOG_APP_KEY environment variables."
        )

    query_parts = [metric_name]
    filter_clauses = []
    for dim_key, dim_values in dimension_filters.items():
        if len(dim_values) == 1:
            filter_clauses.append(f"{dim_key}:{dim_values[0]}")
        else:
            filter_clauses.append(f"{dim_key}:{{{','.join(dim_values)}}}")

    if filter_clauses:
        query_parts.append("{" + " AND ".join(filter_clauses) + "}")

    query_str = f"{aggregation}:{' '.join(query_parts)}"

    payload = {
        "query": query_str,
        "from": int(start_time.timestamp()),
        "to": int(end_time.timestamp()),
    }

    session = create_datadog_session()
    api_url = f"{DATADOG_API_BASE}/api/v1/query"

    response = session.get(api_url, params=payload, timeout=30)
    response.raise_for_status()

    raw_data = response.json()
    data_points = normalize_datadog_response(raw_data)

    return data_points


def filter_metric_dimensions_with_request(
    request: MetricFilter,
) -> List[MetricDataPoint]:
    return filter_metric_dimensions(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        dimension_filters=request.dimension_filters,
        aggregation=request.aggregation,
        interval=request.interval,
    )
