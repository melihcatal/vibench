import os
from google.cloud import monitoring_v3

def summarize_metric_trends_or_anomalies(
    project_id: str,
    metric_type: str,
    end_time_seconds: int,
    end_time_nanos: int,
    minutes: int,
):
    """Summarizes recent metric trends or anomalies using Google Cloud Monitoring.
    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of the metric to query (e.g., "compute.googleapis.com/instance/cpu/usage_time").
        end_time_seconds: The end time of the time window in seconds since epoch.
        end_time_nanos: The nanoseconds part of the end time.
        minutes: The duration of the time window in minutes.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    now = monitoring_v3.types.TimeInterval()
    now.end_time.seconds = end_time_seconds
    now.end_time.nanos = end_time_nanos
    now.start_time.seconds = end_time_seconds - (minutes * 60)
    now.start_time.nanos = end_time_nanos
    query = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_type}"',
            "interval": now,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    return {"status": "success", "message": "Metric query initiated.", "time_series": list(query)}