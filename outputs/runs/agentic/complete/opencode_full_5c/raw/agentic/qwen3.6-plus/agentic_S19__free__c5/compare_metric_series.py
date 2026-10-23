import math
from datetime import datetime
from typing import Dict, List, Optional

import requests

from observability_client import (
    DATADOG_API_BASE,
    create_datadog_session,
    validate_datadog_credentials,
)
from observability_models import (
    MetricComparisonResult,
    MetricDataPoint,
    MetricSeries,
    normalize_datadog_response,
)


def _build_query(
    metric_name: str, aggregation: str, dimensions: Optional[Dict[str, str]]
) -> str:
    query = f"{aggregation}:{metric_name}"
    if dimensions:
        dim_parts = []
        for k, v in dimensions.items():
            dim_parts.append(f"{k}:{v}")
        query = f"{query}{{{' AND '.join(dim_parts)}}}"
    return query


def _fetch_series(
    session: requests.Session,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    aggregation: str,
    dimensions: Optional[Dict[str, str]],
    resource_id: Optional[str],
) -> MetricSeries:
    query = _build_query(metric_name, aggregation, dimensions)
    payload = {
        "query": query,
        "from": int(start_time.timestamp()),
        "to": int(end_time.timestamp()),
    }

    api_url = f"{DATADOG_API_BASE}/api/v1/query"
    response = session.get(api_url, params=payload, timeout=30)
    response.raise_for_status()

    raw_data = response.json()
    data_points = normalize_datadog_response(raw_data)

    return MetricSeries(
        metric_name=metric_name,
        dimensions=dimensions or {},
        resource_id=resource_id,
        data_points=data_points,
    )


def _compute_correlation(values_a: List[float], values_b: List[float]) -> float:
    n = min(len(values_a), len(values_b))
    if n < 2:
        return 0.0

    a = values_a[:n]
    b = values_b[:n]

    mean_a = sum(a) / n
    mean_b = sum(b) / n

    cov = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(n)) / n
    std_a = math.sqrt(sum((x - mean_a) ** 2 for x in a) / n)
    std_b = math.sqrt(sum((x - mean_b) ** 2 for x in b) / n)

    if std_a == 0 or std_b == 0:
        return 0.0

    return cov / (std_a * std_b)


def compare_metric_series(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimensions_a: Optional[Dict[str, str]] = None,
    dimensions_b: Optional[Dict[str, str]] = None,
    resource_id_a: Optional[str] = None,
    resource_id_b: Optional[str] = None,
    aggregation: str = "avg",
) -> MetricComparisonResult:
    if not validate_datadog_credentials():
        raise ValueError(
            "Datadog credentials not configured. Set DATADOG_API_KEY and DATADOG_APP_KEY environment variables."
        )

    session = create_datadog_session()

    series_a = _fetch_series(
        session=session,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        aggregation=aggregation,
        dimensions=dimensions_a,
        resource_id=resource_id_a,
    )

    series_b = _fetch_series(
        session=session,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        aggregation=aggregation,
        dimensions=dimensions_b,
        resource_id=resource_id_b,
    )

    values_a = [dp.value for dp in series_a.data_points]
    values_b = [dp.value for dp in series_b.data_points]

    min_len = min(len(values_a), len(values_b))
    values_a = values_a[:min_len]
    values_b = values_b[:min_len]

    delta_values = [values_a[i] - values_b[i] for i in range(min_len)]
    delta_percentages = []
    for i in range(min_len):
        if values_b[i] != 0:
            delta_percentages.append(
                (values_a[i] - values_b[i]) / abs(values_b[i]) * 100
            )
        else:
            delta_percentages.append(0.0)

    correlation = _compute_correlation(values_a, values_b)

    return MetricComparisonResult(
        series_a=series_a,
        series_b=series_b,
        delta_values=delta_values,
        delta_percentages=delta_percentages,
        correlation=correlation,
        start_time=start_time,
        end_time=end_time,
    )
