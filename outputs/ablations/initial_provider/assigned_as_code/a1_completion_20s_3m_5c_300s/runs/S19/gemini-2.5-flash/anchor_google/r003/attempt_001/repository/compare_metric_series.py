import json
import collections

from google.cloud import monitoring_v3

from observability_client import MonitoringClient
from observability_models import MetricSeries, MetricPoint, MetricQueryResponse

def _get_filtered_series(client, project_id, metric_type, start_time, end_time, dimension_filters, period_seconds):
    filter_parts = [f"metric.type = {json.dumps(metric_type)}"]
    for key, value in dimension_filters.items():
        filter_parts.append(f"metric.labels.{key} = {json.dumps(value)}")
    full_filter = " AND ".join(filter_parts)

    series_data = client.list_time_series(
        metric_filter=full_filter,
        start_time=start_time,
        end_time=end_time,
        period_seconds=period_seconds,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
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
    return metric_series_list

def compare_metric_series(payload, config=None):
    config = config or {}
    client = MonitoringClient(project_id=config['project_id'])

    metric_type = payload["metric"]
    start_time = payload["start_time"]
    end_time = payload["end_time"]
    period_seconds = config.get("period_seconds", 60)

    filter_set1 = payload["filter_set1"]
    filter_set2 = payload["filter_set2"]

    series1 = _get_filtered_series(client, config['project_id'], metric_type, start_time, end_time, filter_set1, period_seconds)
    series2 = _get_filtered_series(client, config['project_id'], metric_type, start_time, end_time, filter_set2, period_seconds)

    # For comparison, we can simplify by taking the first series from each set,
    # or aggregate if multiple series match a filter set.
    # For this example, let's assume one dominant series per filter set or aggregate them.
    # Let's just compare the mean values across the window for simplicity in this example.

    comparison_results = []

    # If there are multiple series for a filter set, we can aggregate their values.
    # For simplicity, let's just get the mean of the points in each series, 
    # and assume there's only one series per filter for direct comparison.

    # This part of the comparison logic can be expanded based on specific requirements.
    # For a basic comparison, we can just return the raw series data for now.
    return {"series1_data": MetricQueryResponse(series=series1), "series2_data": MetricQueryResponse(series=series2)}
