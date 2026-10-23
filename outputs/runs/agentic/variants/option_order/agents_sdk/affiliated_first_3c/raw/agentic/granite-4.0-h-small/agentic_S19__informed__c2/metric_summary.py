# metric_summary.py

from observability_models import MetricQueryResponse, MetricSummary

def summarize_metric_trends(namespace: str, metric_name: str, start_time: str, end_time: str) -> dict:
    """Retrieve recent data points, then produce a concise summary of trends or anomalies."""
    client = CloudWatchClient()
    request = MetricQueryRequest(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=60,
        Statistics=['SampleCount', 'Average']
    )
    response = client.get_metric_data(request)
    # Assume response follows MetricFilterResponse style with a Datapoints list
    datapoints = response.Datapoints
    return MetricSummary.summarize(datapoints)
