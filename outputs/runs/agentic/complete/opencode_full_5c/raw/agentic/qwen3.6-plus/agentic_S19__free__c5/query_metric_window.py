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
    MetricQueryRequest,
    normalize_datadog_response,
)


def query_metric_window(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    aggregation: str = "avg",
    interval: int = 60,
    dimensions: Optional[Dict[str, str]] = None,
) -> List[MetricDataPoint]:
    if not validate_datadog_credentials():
        raise ValueError(
            "Datadog credentials not configured. Set DATADOG_API_KEY and DATADOG_APP_KEY environment variables."
        )

    query = f"{aggregation}:{metric_name}"
    if dimensions:
        dim_parts = []
        for k, v in dimensions.items():
            dim_parts.append(f"{k}:{v}")
        query = f"{query}{{{' AND '.join(dim_parts)}}}"

    payload = {
        "query": query,
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


def query_metric_window_with_request(
    request: MetricQueryRequest,
) -> List[MetricDataPoint]:
    return query_metric_window(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        aggregation=request.aggregation,
        interval=request.interval,
        dimensions=request.dimensions,
    )
