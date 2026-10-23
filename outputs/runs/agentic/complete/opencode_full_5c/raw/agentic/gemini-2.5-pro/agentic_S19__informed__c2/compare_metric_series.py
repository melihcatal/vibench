import time
from typing import Dict, List
from google.cloud import monitoring_v3
from observability_client import get_gcp_observability_client, get_gcp_project_name
from observability_models import ComparisonRequest, MetricTimeSeries, TimeSeriesPoint


def _create_filter_str(metric_name: str, dimension_filter: Dict[str, str]) -> str:
    filter_parts = [f'metric.type = "{metric_name}"']
    for key, value in dimension_filter.items():
        filter_parts.append(f'metric.labels.{key} = "{value}"')
    return " AND ".join(filter_parts)


def _query_series(client, project_name, filter_str, interval) -> List[MetricTimeSeries]:
    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    series_data = []
    for result in results:
        points = [
            TimeSeriesPoint(
                timestamp=p.interval.end_time.rfc3339(), value=p.value.double_value
            )
            for p in result.points
        ]
        dimensions = {
            label: result.metric.labels[label] for label in result.metric.labels
        }
        series_data.append(
            MetricTimeSeries(
                metric_name=result.metric.type, dimensions=dimensions, points=points
            )
        )
    return series_data


def compare_metric_series(
    request: ComparisonRequest,
) -> Dict[str, List[MetricTimeSeries]]:
    client = get_gcp_observability_client(request.project_id)
    if not client:
        return {"series1": [], "series2": []}

    project_name = get_gcp_project_name(request.project_id)
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {
                "seconds": seconds - (request.minutes_ago * 60),
                "nanos": nanos,
            },
        }
    )

    filter1_str = _create_filter_str(request.metric_name, request.filter1)
    filter2_str = _create_filter_str(request.metric_name, request.filter2)

    series1_data = _query_series(client, project_name, filter1_str, interval)
    series2_data = _query_series(client, project_name, filter2_str, interval)

    return {"series1": series1_data, "series2": series2_data}
