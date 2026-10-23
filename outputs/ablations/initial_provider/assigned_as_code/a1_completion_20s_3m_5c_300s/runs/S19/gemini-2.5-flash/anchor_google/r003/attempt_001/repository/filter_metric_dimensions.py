import json

from google.cloud import monitoring_v3

from observability_client import MonitoringClient
from observability_models import MetricSeries, MetricPoint, MetricQueryResponse

def filter_metric_dimensions(payload, config=None):
    config = config or {}
    client = MonitoringClient(project_id=config['project_id'])

    metric_type = payload["metric"]
    start_time = payload["start_time"]
    end_time = payload["end_time"]
    period_seconds = config.get("period_seconds", 60)
    dimension_filters = payload.get("dimensions", {})

    filter_parts = [f"metric.type = {json.dumps(metric_type)}"]
    for key, value in dimension_filters.items():
        filter_parts.append(f"metric.labels.{key} = {json.dumps(value)}")

    full_filter = " AND ".join(filter_parts)

    series_data = client.list_time_series(
        metric_filter=full_filter,
        start_time=start_time,
        end_time=end_time,
        period_seconds=period_seconds,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL # Use FULL to get all labels
    )

    metric_series_list = []
    for ts in series_data:
        points = []
        for point in ts.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            points.append(MetricPoint(timestamp=point.interval.end_time.timestamp(), value=float(getattr(point.value, kind))))
        
        metric_series_list.append(MetricSeries(
            resource_labels=dict(ts.resource.labels),
            metric_labels=dict(ts.metric.labels),
            points=sorted(points, key=lambda p: p.timestamp)
        ))

    return MetricQueryResponse(series=metric_series_list)
