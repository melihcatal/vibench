from google.cloud import monitoring_v3
import datetime
from google.protobuf.timestamp_pb2 import Timestamp

def filter_metric_dimensions(project_id: str, metric_type: str, end_time_iso: str, duration_seconds: int, filters: dict):
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

    filter_parts = [f'metric.type = "{metric_type}"']
    for key, value in filters.items():
        filter_parts.append(f'{key} = "{value}"')
    
    full_filter = " AND ".join(filter_parts)

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": full_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    return [
        {
            "metric": dict(series.metric),
            "resource": dict(series.resource),
            "points": [
                {"interval": {"start_time": p.interval.start_time.isoformat(), "end_time": p.interval.end_time.isoformat()}, "value": dict(p.value)}
                for p in series.points
            ]
        }
        for series in results
    ]
