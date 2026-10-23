"""Retrieve aggregated statistics for a metric over a time window.

Uses Google Cloud Monitoring API (google-cloud-monitoring SDK) with
server-side aggregation (ALIGN_MEAN, ALIGN_SUM, ALIGN_MAX, ALIGN_MIN)
to compute summary statistics for a metric.
Provider signals:
  - google.cloud.monitoring_v3 Aggregation proto
  - google.cloud.monitoring_v3 MetricServiceClient
  - GOOGLE_APPLICATION_CREDENTIALS environment variable
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from google.cloud.monitoring_v3 import (
    Aggregation,
    ListTimeSeriesRequest,
    TimeSeries,
)
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
    compute_series_stats,
    normalize_point_value,
)

# Map friendly aligner names to Google Cloud Monitoring Aggregation.Aligner values.
AGGREGATION_MAP = {
    "mean": Aggregation.Aligner.ALIGN_MEAN,
    "sum": Aggregation.Aligner.ALIGN_SUM,
    "max": Aggregation.Aligner.ALIGN_MAX,
    "min": Aggregation.Aligner.ALIGN_MIN,
    "count": Aggregation.Aligner.ALIGN_COUNT,
    "percentile_99": Aggregation.Aligner.ALIGN_PERCENTILE_99,
}


def aggregate_metric_stats(
    metric_name: str,
    window_minutes: int = 60,
    project_id: Optional[str] = None,
    alignment_period_seconds: int = 60,
    aligner: str = "mean",
    end_time: Optional[datetime] = None,
    config: Optional[ObservabilityConfig] = None,
) -> Dict[str, Dict[str, float]]:
    """Retrieve aggregated statistics for *metric_name* over a time window
    using Google Cloud Monitoring server-side aggregation.

    Parameters
    ----------
    metric_name : str
        Full metric type or shorthand.
    window_minutes : int
        Length of the query window in minutes.
    project_id : str, optional
        GCP project ID.
    alignment_period_seconds : int
        Aggregation bucket size in seconds.
    aligner : str
        One of "mean", "sum", "max", "min", "count", "percentile_99".
    end_time : datetime, optional
        End of the window; defaults to now.
    config : ObservabilityConfig, optional
        Configuration for credentials.

    Returns
    -------
    Dict[str, Dict[str, float]]
        Mapping from resource identifier to aggregation stats
        (count, min, max, mean, sum).
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

    agg = Aggregation()
    agg.alignment_period.seconds = alignment_period_seconds
    agg.per_series_aligner = AGGREGATION_MAP.get(aligner, Aggregation.Aligner.ALIGN_MEAN)

    request = ListTimeSeriesRequest()
    request.name = name
    request.filter = f'metric.type = "{full_metric_type}"'
    request.interval = time_interval
    request.aggregation = agg
    request.view = ListTimeSeriesRequest.TimeSeriesView.FULL

    results: Dict[str, Dict[str, float]] = {}
    for ts in client.list_time_series(request=request):
        series = _convert_timeseries(ts, full_metric_type)
        resource_key = _resource_key(ts)
        results[resource_key] = compute_series_stats(series)

    return results


def _resource_key(ts: TimeSeries) -> str:
    """Derive a readable resource key from a TimeSeries proto."""
    labels = dict(ts.resource.labels) if ts.resource else {}
    instance_id = labels.get("instance_id", labels.get("zone", "unknown"))
    return f"{ts.resource.type}/{instance_id}"


def _convert_timeseries(ts: TimeSeries, metric_type: str) -> MetricSeries:
    """Convert a Google Cloud TimeSeries proto to a normalized MetricSeries."""
    resource_labels = {}
    if ts.resource:
        resource_labels = dict(ts.resource.labels)

    points: List[MetricDataPoint] = []
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


if __name__ == "__main__":
    stats = aggregate_metric_stats("cpu/utilization", window_minutes=30, aligner="mean")
    for resource, agg in stats.items():
        print(f"Resource: {resource}")
        for key, val in agg.items():
            print(f"  {key}: {val}")
