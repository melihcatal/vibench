import time
from typing import List, Dict, Tuple
from datadog_api_client.v2.api.metrics_api import MetricsApi
from observability_client import get_datadog_client
from observability_models import MetricSeries, MetricPoint


def compare_filtered_series(
    metric_name: str,
    filter_a: Dict[str, str],
    filter_b: Dict[str, str],
    minutes_ago: int = 60,
) -> Tuple[List[MetricSeries], List[MetricSeries]]:
    client = get_datadog_client()
    api_instance = MetricsApi(client)

    now = int(time.time())
    start_time = now - (minutes_ago * 60)

    filter_str_a = ",".join([f"{k}:{v}" for k, v in filter_a.items()])
    query_a = f"{metric_name}{{{filter_str_a}}}"

    filter_str_b = ",".join([f"{k}:{v}" for k, v in filter_b.items()])
    query_b = f"{metric_name}{{{filter_str_b}}}"

    response = api_instance.query_timeseries_data(
        body={
            "data": {
                "type": "timeseries_request",
                "attributes": {
                    "queries": [
                        {"data_source": "metrics", "name": "a", "query": query_a},
                        {"data_source": "metrics", "name": "b", "query": query_b},
                    ],
                    "from": start_time * 1000,
                    "to": now * 1000,
                },
            }
        }
    )

    series_a_results = []
    series_b_results = []
    if response.data.attributes.series:
        for series in response.data.attributes.series:
            query_name = series.query_index
            points = [MetricPoint(timestamp=p[0], value=p[1]) for p in series.pointlist]
            metric_series = MetricSeries(
                metric_name=series.metric,
                points=points,
                tags=dict(tag.split(":", 1) for tag in series.group_tags),
            )
            if query_name == 0:
                series_a_results.append(metric_series)
            elif query_name == 1:
                series_b_results.append(metric_series)

    return series_a_results, series_b_results
