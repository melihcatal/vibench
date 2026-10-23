"""Compare metric values for two resources or dimension filters over the same window.

Uses Google Cloud Monitoring API (google-cloud-monitoring SDK) to fetch
two separate metric series and compute a side-by-side comparison including
delta and ratio statistics.
Provider signals:
  - google.cloud.monitoring_v3 MetricServiceClient
  - google.cloud.monitoring_v3.ListTimeSeriesRequest
  - GOOGLE_APPLICATION_CREDENTIALS environment variable
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from google.cloud.monitoring_v3 import ListTimeSeriesRequest
from google.cloud.monitoring_v3.services.metric_service import MetricServiceClient

from observability_client import (
    ObservabilityConfig,
    build_metric_type,
    build_monitored_resource_name,
    create_metric_service_client,
)
from observability_models import (
    MetricDataPoint,
    MetricQueryParams,
    MetricSeries,
    build_label_filter,
    compute_series_stats,
    normalize_point_value,
)


@dataclass
class ComparisonResult:
    """Result of comparing two metric series."""

    series_a_name: str
    series_b_name: str
    stats_a: Dict[str, float]
    stats_b: Dict[str, float]
    delta_mean: float
    ratio_mean: float
    series_a: MetricSeries
    series_b: MetricSeries


def compare_metric_series(
    metric_name: str,
    filter_a: Dict[str, str],
    filter_b: Dict[str, str],
    window_minutes: int = 60,
    project_id: Optional[str] = None,
    alignment_period_seconds: int = 60,
    end_time: Optional[datetime] = None,
    config: Optional[ObservabilityConfig] = None,
) -> ComparisonResult:
    """Compare metric values for two sets of dimension filters over the
    same time window using Google Cloud Monitoring.

    Parameters
    ----------
    metric_name : str
        Full metric type or shorthand.
    filter_a : dict
        First dimension filter set (e.g. {"zone": "us-east1-b"}).
    filter_b : dict
        Second dimension filter set (e.g. {"zone": "us-west1-a"}).
    window_minutes : int
        Length of the query window in minutes.
    project_id : str, optional
        GCP project ID.
    alignment_period_seconds : int
        Alignment period in seconds.
    end_time : datetime, optional
        End of window; defaults to now.
    config : ObservabilityConfig, optional
        Configuration for credentials.

    Returns
    -------
    ComparisonResult
        Comparison with stats, deltas, and ratios.
    """
    cfg = config or ObservabilityConfig(project_id=project_id)
    resolved_project = cfg.ensure_project()

    client: MetricServiceClient = create_metric_service_client(cfg)
    name = build_monitored_resource_name(resolved_project)
    full_metric_type = build_metric_type(metric_name)

    params = MetricQueryParams(
        metric_name=full_metric_type,
        window_minutes=window_minutes,
        alignment_period_seconds=alignment_period_seconds,
        end_time=end_time,
    )
    time_interval = params.to_time_interval()

    series_a = _fetch_filtered_series(
        client, name, full_metric_type, filter_a, time_interval, "SeriesA"
    )
    series_b = _fetch_filtered_series(
        client, name, full_metric_type, filter_b, time_interval, "SeriesB"
    )

    stats_a = compute_series_stats(series_a)
    stats_b = compute_series_stats(series_b)

    delta_mean = stats_a["mean"] - stats_b["mean"]
    ratio_mean = (stats_a["mean"] / stats_b["mean"]) if stats_b["mean"] != 0 else float("inf")

    return ComparisonResult(
        series_a_name=_filter_label(filter_a),
        series_b_name=_filter_label(filter_b),
        stats_a=stats_a,
        stats_b=stats_b,
        delta_mean=delta_mean,
        ratio_mean=ratio_mean,
        series_a=series_a,
        series_b=series_b,
    )


def _fetch_filtered_series(
    client: MetricServiceClient,
    name: str,
    metric_type: str,
    dimension_filters: Dict[str, str],
    time_interval,
    series_label: str,
) -> MetricSeries:
    """Fetch a single filtered metric series."""
    label_filter = build_label_filter(dimension_filters)
    filter_expr = f'metric.type = "{metric_type}"'
    if label_filter:
        filter_expr += f" AND {label_filter}"

    request = ListTimeSeriesRequest()
    request.name = name
    request.filter = filter_expr
    request.interval = time_interval
    request.view = ListTimeSeriesRequest.TimeSeriesView.FULL

    points: List[MetricDataPoint] = []
    resource_labels: Dict[str, str] = {}

    for ts in client.list_time_series(request=request):
        if ts.resource:
            resource_labels = dict(ts.resource.labels)
        for point in ts.points:
            ts_dt = datetime.utcfromtimestamp(
                point.interval.end_time.seconds + point.interval.end_time.nanos / 1e9
            )
            value = normalize_point_value(point.value)
            points.append(MetricDataPoint(timestamp=ts_dt, value=value))

    return MetricSeries(
        metric_type=metric_type,
        resource_labels=resource_labels,
        points=points,
    )


def _filter_label(filters: Dict[str, str]) -> str:
    return ",".join(f"{k}={v}" for k, v in sorted(filters.items()))


if __name__ == "__main__":
    result = compare_metric_series(
        "cpu/utilization",
        filter_a={"zone": "us-east1-b"},
        filter_b={"zone": "us-west1-a"},
        window_minutes=30,
    )
    print(f"Comparing {result.series_a_name} vs {result.series_b_name}")
    print(f"Mean delta: {result.delta_mean:.4f}")
    print(f"Mean ratio: {result.ratio_mean:.4f}")
