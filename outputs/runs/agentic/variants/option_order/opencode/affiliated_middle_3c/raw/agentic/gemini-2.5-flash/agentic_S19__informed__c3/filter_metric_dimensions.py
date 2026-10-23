from observability_client import GoogleCloudMonitoringClient
from observability_models import MetricQueryRequest, MetricSeries
from typing import List


def query_metric_data_filtered_by_dimensions(
    project_id: str,
    metric_type: str,
    start_time: str,
    end_time: str,
    dimension_filters: str,  # e.g., 'resource.labels.instance_name = "my-instance"'
) -> List[MetricSeries]:
    client = GoogleCloudMonitoringClient()
    filter_string = f"{dimension_filters}"
    request = MetricQueryRequest(
        project_id=project_id,
        metric_type=metric_type,
        interval_start_time=start_time,
        interval_end_time=end_time,
        filter_string=filter_string,
    )
    return client.query_time_series_data(request)
