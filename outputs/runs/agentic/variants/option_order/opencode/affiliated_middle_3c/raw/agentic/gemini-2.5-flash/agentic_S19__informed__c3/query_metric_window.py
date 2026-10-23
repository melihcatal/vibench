from observability_client import GoogleCloudMonitoringClient
from observability_models import MetricQueryRequest, MetricSeries
from typing import List


def query_recent_metric_datapoints(
    project_id: str,
    metric_type: str,
    start_time: str,
    end_time: str,
    filter_string: str = "",
) -> List[MetricSeries]:
    client = GoogleCloudMonitoringClient()
    request = MetricQueryRequest(
        project_id=project_id,
        metric_type=metric_type,
        interval_start_time=start_time,
        interval_end_time=end_time,
        filter_string=filter_string,
    )
    return client.query_time_series_data(request)
