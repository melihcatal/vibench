from datetime import datetime, timedelta, timezone
from google.protobuf.duration_pb2 import Duration
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_monitoring_client, get_project_name
from google.cloud.monitoring_v3.types import Aggregation

def aggregate_metric_stats(
    metric_type: str, 
    minutes_ago: int, 
    alignment_period_seconds: int = 60
) -> dict:
    """
    Retrieves aggregated statistics for a metric over a time window.
    
    Args:
        metric_type: The metric identifier.
        minutes_ago: The time window in minutes from now.
        alignment_period_seconds: The period to align data points to, in seconds.

    Returns:
        A dictionary containing the aggregated time series data.
    """
    client = get_monitoring_client()
    project_name = get_project_name()

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": Timestamp(seconds=int(now.timestamp())),
            "start_time": Timestamp(seconds=int(start_time.timestamp())),
        }
    )
    
    aggregation = Aggregation(
        alignment_period=Duration(seconds=alignment_period_seconds),
        per_series_aligner=Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=["metric.label.instance_name"],
    )

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=f'metric.type = "{metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )
    
    results = client.list_time_series(request=request)

    output_series = []
    for result in results:
        points = [
            {"timestamp": p.interval.end_time.rfc3339(), "value": p.value.double_value}
            for p in result.points
        ]
        output_series.append({
            "metric_labels": dict(result.metric.labels),
            "points": points
        })

    return {"aggregated_series": output_series}
