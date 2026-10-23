import datetime
from google.cloud import monitoring_v3

def compare_metric_series(
    project_id: str,
    metric_type: str,
    resource_type: str,
    filter_a: str,
    filter_b: str,
    end_time: datetime.datetime,
    minutes: int,
):
    """
    Compares metric values for two resources or dimension filters over the same window
    using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The metric descriptor type (e.g., "compute.googleapis.com/instance/cpu/utilization").
        resource_type: The monitored resource type (e.g., "gce_instance").
        filter_a: The Monitoring filter string for the first series.
                  Example: 'resource.labels.instance_name = "instance-1"'
        filter_b: The Monitoring filter string for the second series.
                  Example: 'resource.labels.instance_name = "instance-2"'
        end_time: The end of the time window for the query (datetime object).
        minutes: The duration of the time window in minutes.

    Returns:
        A dictionary containing the time series data for filter_a and filter_b.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - datetime.timedelta(minutes=minutes)

    interval = monitoring_v3.TimeInterval(
        end_time=end_time,
        start_time=start_time,
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 60},  # 1-minute alignment
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    )

    # Function to get time series data for a given filter
    def get_time_series(filter_string: str):
        full_filter = f'metric.type = "{metric_type}" AND resource.type = "{resource_type}" AND {filter_string}'
        response = client.list_time_series(
            request={
                "name": project_name,
                "filter": full_filter,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )
        return response

    print(f"Fetching data for filter A: {filter_a}")
    series_a = get_time_series(filter_a)
    print(f"Fetching data for filter B: {filter_b}")
    series_b = get_time_series(filter_b)

    # In a real application, you would implement specific comparison logic here.
    # For now, we return the raw series data.
    return {
        "series_a": series_a,
        "series_b": series_b,
    }

