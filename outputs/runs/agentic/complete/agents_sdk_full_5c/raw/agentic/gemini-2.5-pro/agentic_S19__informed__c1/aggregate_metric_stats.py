import time
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricSeries, to_metric_series_list

def retrieve_aggregated_stats(
    project_id: str,
    metric_type: str,
    minutes_ago: int = 60,
    aggregation_minutes: int = 5,
) -> list[MetricSeries]:
    """
    Retrieves aggregated statistics for a metric over a time window.

    Args:
        project_id: The Google Cloud project ID.
        metric_type: The identifier of the metric.
        minutes_ago: The total time window to query in minutes.
        aggregation_minutes: The duration of each aggregation window in minutes.

    Returns:
        A list of MetricSeries objects with aggregated data.
    """
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": seconds - (minutes_ago * 60), "nanos": nanos},
        }
    )

    # Documentation on aggregation:
    # https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/list#Aggregation
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": aggregation_minutes * 60},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_NONE,
        }
    )

    request = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        "aggregation": aggregation,
    }

    results = client.list_time_series(request)
    return to_metric_series_list(results)

if __name__ == '__main__':
    # This is an example and will not be executed in the test environment.
    proj_id = get_project_id()
    metric = "compute.googleapis.com/instance/cpu/usage_time"

    print(f"Querying aggregated stats for metric '{metric}' for project '{proj_id}'...")
    aggregated_series = retrieve_aggregated_stats(proj_id, metric, minutes_ago=60, aggregation_minutes=10)
    
    if not aggregated_series:
        print("No data found for aggregation.")
    else:
        for series in aggregated_series:
            print("--- Aggregated Time Series ---")
            print(f"Resource Labels: {series.resource_labels}")
            print(f"Found {len(series.points)} aggregated points.")
            for point in series.points:
                 print(f"  {point.timestamp.ToDatetime()}: Mean value = {point.value}")
