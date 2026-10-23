from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import QueryResult, TimeSeries, TimeSeriesPoint


def get_series(client, project_name, metric_type, dimensions, interval):
    dimension_filters = " AND ".join(
        [f'resource.labels.{key} = "{value}"' for key, value in dimensions.items()]
    )
    filter_string = f'metric.type = "{metric_type}" AND {dimension_filters}'

    request = {
        "name": project_name,
        "filter": filter_string,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }
    return client.list_time_series(request)


def compare_filtered_metrics(
    metric_type: str,
    dimensions1: Dict[str, str],
    dimensions2: Dict[str, str],
    minutes: int = 60,
) -> Tuple[QueryResult, QueryResult]:
    client = get_monitoring_client()
    project_id = get_project_id()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    results1 = get_series(client, project_name, metric_type, dimensions1, interval)
    results2 = get_series(client, project_name, metric_type, dimensions2, interval)

    def to_query_result(results):
        query_result = QueryResult()
        for result in results:
            ts = TimeSeries(
                metric_name=result.metric.type,
                resource_labels=dict(result.resource.labels),
            )
            for point in result.points:
                ts.points.append(
                    TimeSeriesPoint(
                        timestamp=point.interval.end_time.timestamp(),
                        value=point.value.double_value,
                    )
                )
            query_result.series.append(ts)
        return query_result

    return to_query_result(results1), to_query_result(results2)
