
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

def aggregate_metric_stats(project_id: str, metric_type: str, window_minutes: int):
    """Retrieves aggregated statistics for a metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud Project ID.
        metric_type: The type of metric to query (e.g., "compute.googleapis.com/instance/cpu/utilization").
        window_minutes: The duration of the aggregation window in minutes.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.datetime.now(datetime.timezone.utc)
    end_time = Timestamp()
    end_time.FromDatetime(now)
    start_time = Timestamp()
    start_time.FromDatetime(now - datetime.timedelta(minutes=window_minutes))

    interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

    aggregation = monitoring_v3.Aggregation(
        alignment_period=
            {"seconds": window_minutes * 60},
        per_series_aligner=
            monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=
            monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=["resource.zone", "resource.labels.instance_name"],
    )

    results = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    print(f"Aggregated metric statistics for project {project_id}, metric {metric_type}:")
    for result in results:
        print(result)

if __name__ == '__main__':
    # Replace with your actual Google Cloud Project ID and metric type
    PROJECT_ID = "your-gcp-project-id"
    METRIC_TYPE = "compute.googleapis.com/instance/cpu/utilization"
    WINDOW_MINUTES = 60

    print(f"To run this example, ensure you have authenticated with Google Cloud and installed the Google Cloud Monitoring client library: pip install google-cloud-monitoring")
    print(f"Also, replace 'your-gcp-project-id' with your actual project ID and adjust METRIC_TYPE as needed.")
    # aggregate_metric_stats(PROJECT_ID, METRIC_TYPE, WINDOW_MINUTES)
