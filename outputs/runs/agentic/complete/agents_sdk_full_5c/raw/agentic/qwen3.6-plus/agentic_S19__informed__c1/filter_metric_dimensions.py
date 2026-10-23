"""Query metric data filtered by resource labels or dimensions.

Uses Google Cloud Monitoring API (google-cloud-monitoring SDK) to
apply label/dimension filters when querying metric time-series data.
Provider signals:
  - google.cloud.monitoring_v3 MetricServiceClient
  - google.cloud.monitoring_v3.ListTimeSeriesRequest with label filters
  - GOOGLE_APPLICATION_CREDENTIALS environment variable
"""

from __future__ import annotations

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
    normalize_point_value,
)


def filter_metric_dimensions(
    metric_name: str,
    dimension_filters: Dict[str, str],
    window_minutes: int = 60,
    project_id: Optional[str] = None,
    alignment_period_seconds: int = 60,
    end_time: Optional[datetime] = None,
    config: Optional[ObservabilityConfig] = None,
) -> List[MetricSeries]:
    """Query metric data for *metric_name* filtered by resource or metric
    labels using Google Cloud Monitoring.

    Parameters
    ----------
    metric_name : str
        Full metric type or shorthand.
    dimension_filters : dict
        Key-value pairs for filtering, e.g.
        {"zone": "us-central1-a", "instance_id": "my-vm-1"}.
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
    List[MetricSeries]
        Filtered metric series with aligned datapoints.
    """
    cfg = config or ObservabilityConfig(project_id=project_id)
    resolved_project = cfg.ensure_project()

    client: MetricServiceClient = create_metric_service_client(cfg)
    name = build_monitored_resource_name(resolved_project)
    full_metric_type = build_metric_type(metric_name)

    label_filter = build_label_filter(dimension_filters)
    filter_expr = f'metric.type = "{full_metric_type}"'
    if label_filter:
        filter_expr += f" AND {label_filter}"

    params = MetricQueryParams(
        metric_name=full_metric_type,
        window_minutes=window_minutes,
        alignment_period_seconds=alignment_period_seconds,
        labels=dimension_filters,
        end_time=end_time,
    )
    time_interval = params.to_time_interval()

    request = ListTimeSeriesRequest()
    request.name = name
    request.filter = filter_expr
    request.interval = time_interval
    request.view = ListTimeSeriesRequest.TimeSeriesView.FULL

    series_list: List[MetricSeries] = []
    for ts in client.list_time_series(request=request):
        series = _convert_timeseries(ts, full_metric_type)
        series_list.append(series)

    return series_list


def _convert_timeseries(ts, metric_type: str) -> MetricSeries:
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
        metric_labels = dict(point.ToDict().get("metric", {}).get("labels", {})) if hasattr(point, "ToDict") else {}
        points.append(MetricDataPoint(timestamp=ts_dt, value=value, labels=metric_labels))

    return MetricSeries(
        metric_type=metric_type,
        resource_labels=resource_labels,
        points=points,
    )


if __name__ == "__main__":
    results = filter_metric_dimensions(
        "cpu/utilization",
        dimension_filters={"zone": "us-central1-a"},
        window_minutes=30,
    )
    for series in results:
        print(f"Series {series.metric_type} resource={series.resource_labels}")
        for dp in series.points:
            print(f"  {dp.timestamp} -> {dp.value}")
