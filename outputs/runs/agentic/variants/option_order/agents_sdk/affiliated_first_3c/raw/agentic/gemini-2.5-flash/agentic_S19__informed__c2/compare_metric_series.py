import datetime
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricQuery, TimeSeriesData
from typing import List, Tuple

def compare_metric_series(query_1: MetricQuery, query_2: MetricQuery) -> Tuple[List[TimeSeriesData], List[TimeSeriesData]]:
    """
    Compares metric values for two resources or dimension filters over the same window using Google Cloud Monitoring.
    Each query represents a different series to compare.
    """
    client = get_monitoring_client()
    project_id = query_1.project_id or get_project_id() # Assuming same project for comparison
    project_name = f"projects/{project_id}"

    def _fetch_series(query: MetricQuery) -> List[TimeSeriesData]:
        interval = monitoring_v3.TimeInterval(
            end_time={"seconds": int(query.end_time.timestamp())},
            start_time={"seconds": int(query.start_time.timestamp())},
        )

        metric_filter = f'metric.type = "{query.metric_type}"'
        if query.filters:
            metric_filter += f' AND {query.filters}'

        results = client.list_time_series(
            name=project_name,
            filter=metric_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        time_series_data_list = []
        for time_series in results:
            points = []
            for point in time_series.points:
                point_value = None
                if point.value.double_value is not None:
                    point_value = point.value.double_value
                elif point.value.int64_value is not None:
                    point_value = point.value.int64_value
                elif point.value.string_value is not None:
                    point_value = point.value.string_value
                elif point.value.bool_value is not None:
                    point_value = point.value.bool_value

                points.append({
                    "timestamp": point.interval.end_time.timestamp(),
                    "value": point_value
                })
            time_series_data_list.append(TimeSeriesData(
                points=points,
                resource_labels=dict(time_series.resource.labels),
                metric_labels=dict(time_series.metric.labels)
            ))
        return time_series_data_list

    series_1 = _fetch_series(query_1)
    series_2 = _fetch_series(query_2)

    return series_1, series_2
