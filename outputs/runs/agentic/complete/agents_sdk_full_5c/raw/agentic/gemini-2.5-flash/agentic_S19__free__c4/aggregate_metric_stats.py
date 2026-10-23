from google.cloud import monitoring_v3
from datetime import datetime, timedelta

def aggregate_metric_stats(project_id: str, metric_type: str, minutes_ago: int = 60):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time.timestamp())},
        start_time={'seconds': int(start_time.timestamp())}
    )

    query_filter = f'metric.type = "{metric_type}"'

    aggregation = monitoring_v3.Aggregation(
        alignment_period={'seconds': 60},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=["resource.label.instance_name"]
    )

    result = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    aggregated_data = []
    for series in result:
        for point in series.points:
            aggregated_data.append({
                "metric": series.metric.type,
                "resource_labels": dict(series.resource.labels),
                "value": point.value.double_value or point.value.int64_value,
                "timestamp": point.interval.end_time.ToDatetime().isoformat(),
            })
    return aggregated_data
