from google.cloud import monitoring_v3
import datetime
from google.protobuf.timestamp_pb2 import Timestamp

def aggregate_metric_stats(project_id: str, metric_type: str, end_time_iso: str, duration_seconds: int, aggregator: str):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    end_dt = datetime.datetime.fromisoformat(end_time_iso.replace('Z', '+00:00'))
    end_time_timestamp = Timestamp()
    end_time_timestamp.FromDatetime(end_dt)

    start_time_timestamp = Timestamp()
    start_dt = end_dt - datetime.timedelta(seconds=duration_seconds)
    start_time_timestamp.FromDatetime(start_dt)

    interval = monitoring_v3.TimeInterval(
        end_time=end_time_timestamp,
        start_time=start_time_timestamp,
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": duration_seconds}, # Aggregate over the whole window
        per_series_aligner=getattr(monitoring_v3.Aggregation.Aligner, aggregator.upper()),
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_NONE, # No cross-series reduction for individual series stats
        group_by_fields=["resource.metric_kind", "resource.type", "metric.type"] # Basic grouping
    )

    query = f'metric.type = "{metric_type}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": query,
            "interval": interval,
            "aggregation": aggregation,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    aggregated_data = []
    for series in results:
        if series.points:
            point_value = next(iter(series.points[0].value.values()))
            aggregated_data.append({
                "metric": dict(series.metric),
                "resource": dict(series.resource),
                "aggregated_value": point_value,
                "interval": {"start_time": series.points[0].interval.start_time.isoformat(), "end_time": series.points[0].interval.end_time.isoformat()}
            })
    return aggregated_data
