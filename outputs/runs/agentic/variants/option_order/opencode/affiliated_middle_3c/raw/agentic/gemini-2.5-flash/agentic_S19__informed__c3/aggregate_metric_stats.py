from observability_client import GoogleCloudMonitoringClient
from observability_models import MetricQueryRequest, MetricAggregate
from typing import List


def get_aggregated_metric_statistics(
    project_id: str,
    metric_type: str,
    start_time: str,
    end_time: str,
    reducer: str = "REDUCE_MEAN",
    alignment_period: str = "60s",
    filter_string: str = "",
) -> List[MetricAggregate]:
    client = GoogleCloudMonitoringClient()
    request = MetricQueryRequest(
        project_id=project_id,
        metric_type=metric_type,
        interval_start_time=start_time,
        interval_end_time=end_time,
        aggregation_reducer=reducer,
        aggregation_alignment_period=alignment_period,
        filter_string=filter_string,
    )
    series_list = client.query_time_series_data(request)

    aggregated_results = []
    for series in series_list:
        if series.points:
            # Assuming a single aggregate value per series for simplicity after aggregation
            # In a real scenario, you might compute statistics from the points if not directly provided by the API
            # For Google Cloud Monitoring, the API returns already aggregated points based on the reducer
            for point in series.points:
                aggregated_results.append(
                    MetricAggregate(
                        statistic=reducer.replace("REDUCE_", ""),
                        value=point.value,
                        timestamp=point.timestamp,
                    )
                )
    return aggregated_results
