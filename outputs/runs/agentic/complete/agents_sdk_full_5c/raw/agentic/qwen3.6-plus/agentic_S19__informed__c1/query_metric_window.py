"""Query recent datapoints for a named metric over a time window.

Uses Google Cloud Monitoring API (google-cloud-monitoring SDK) to retrieve
raw time-series datapoints for a specific metric within a configurable window.
Provider signals:
  - google.cloud.monitoring_v3 MetricServiceClient
  - google.api.monitoredres_pb2, monitoring_pb2
  - GOOGLE_APPLICATION_CREDENTIALS environment variable
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from google.cloud.monitoring_v3 import (
    ListTimeSeriesRequest,
    TimeSeries,
)
from google.cloud.monitoring_v3.services.metric_service import MetricServiceClient
from google.api import monitoredres_pb2

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
    normalize_point_value,
)


def query_metric_window(
    metric_name: str,
    window_minutes: int = 60,
    project_id: Optional[str] = None,
    alignment_period_seconds: int = 60,
    end_time: Optional[datetime] = None,
    config: Optional[ObservabilityConfig] = None,
) -> List[MetricSeries]:
    """Query recent datapoints for *metric_name* over a time window using
    Google Cloud Monitoring.

    Parameters
    ----------
    metric_name : str
        Full metric type (e.g. "compute.googleapis.com/instance/cpu/utilization")
        or shorthand ("cpu/utilization").
    window_minutes : int
        Length of the query window in minutes.
    project_id : str, optional
        GCP project ID; falls back to ObservabilityConfig.
    alignment_period_seconds : int
        Period for aggregating datapoints.
    end_time : datetime, optional
        End of the time window; defaults to now.
    config : ObservabilityConfig, optional
        Configuration instance for credential resolution.

    Returns
    -------
    List[MetricSeries]
        Normalized series objects containing aligned datapoints.
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

    request = ListTimeSeriesRequest()
    request.name = name
    request.filter = f'metric.type = "{full_metric_type}"'
    request.interval = time_interval
    request.view = ListTimeSeriesRequest.TimeSeriesView.FULL

    series_list: List[MetricSeries] = []
    for ts in client.list_time_series(request=request):
        series = _convert_timeseries(ts, full_metric_type)
        series_list.append(series)

    return series_list


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
        labels = dict(point.interval.end_time.ToDict()) if hasattr(point.interval, "ToDict") else {}
        points.append(MetricDataPoint(timestamp=ts_dt, value=value, labels=labels))

    return MetricSeries(
        metric_type=metric_type,
        resource_labels=resource_labels,
        points=points,
    )


if __name__ == "__main__":
    results = query_metric_window("cpu/utilization", window_minutes=30)
    for series in results:
        print(f"Series {series.metric_type} labels={series.resource_labels}")
        for dp in series.points:
            print(f"  {dp.timestamp} -> {dp.value}")
