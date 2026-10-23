from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2

def compare_metric_series(project_id: str, metric_type: str, interval_end_time: int, interval_start_time: int, filter1: str, filter2: str):
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(project_id)

    interval = monitoring_v3.TimeInterval(
        end_time=timestamp_pb2.Timestamp(seconds=interval_end_time),
        start_time=timestamp_pb2.Timestamp(seconds=interval_start_time),
    )

    # Query for the first series
    series1 = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_type}" AND {filter1}',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    # Query for the second series
    series2 = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_type}" AND {filter2}',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    
    # In a real-world scenario, you would process and compare series1 and series2 here.
    # For this task, we will just return the raw time series data for demonstration.
    return {"series1": list(series1), "series2": list(series2)}
