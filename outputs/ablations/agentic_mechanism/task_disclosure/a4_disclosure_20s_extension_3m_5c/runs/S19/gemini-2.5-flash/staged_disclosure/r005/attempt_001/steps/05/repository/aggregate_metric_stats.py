import os
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2

def get_metric_stats(project_id: str, metric_type: str, hours: int = 1) -> dict:
    """
    Retrieves aggregated statistics for a metric over a specified time window using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/utilization").
        hours: The number of hours to look back for data. Defaults to 1 hour.

    Returns:
        A dictionary containing aggregated statistics (mean, min, max) for the metric.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = timestamp_pb2.Timestamp()
    now.GetCurrentTime()
    interval = monitoring_v3.TimeInterval(
        end_time=now,
        start_time=timestamp_pb2.Timestamp(seconds=now.seconds - (hours * 3600))
    )

    query_params = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        "aggregation": monitoring_v3.Aggregation(
            alignment_period=timestamp_pb2.Duration(seconds=600), # 10 minutes
            per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
            group_by_fields=["metric.labels.instance_name"] # Example, adjust as needed
        )
    }

    results = client.list_time_series(request=query_params)

    # Basic aggregation (you might want more sophisticated logic based on your needs)
    values = []
    for page in results.pages:
        for series in page:
            for point in series.points:
                if point.value.HasField("double_value"):
                    values.append(point.value.double_value)
                elif point.value.HasField("int64_value"):
                    values.append(point.value.int64_value)

    if not values:
        return {"message": "No data found for the specified metric and time window."}

    return {
        "mean": sum(values) / len(values),
        "min": min(values),
        "max": max(values)
    }

if __name__ == "__main__":
    # Example usage: Replace with your project ID and a valid metric type
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # run `gcloud auth application-default login`
    # project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    # metric_type = "logging.googleapis.com/log_entry_count"
    # stats = get_metric_stats(project_id, metric_type, hours=24)
    # print(stats)
    pass
