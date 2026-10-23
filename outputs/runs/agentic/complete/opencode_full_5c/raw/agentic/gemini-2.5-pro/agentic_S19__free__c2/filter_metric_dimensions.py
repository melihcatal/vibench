import time
from typing import List, Dict
from datadog_api_client.v2.api.metrics_api import MetricsApi
from observability_client import get_datadog_client
from observability_models import MetricSeries, MetricPoint


def query_metrics_by_dimension(
    metric_name: str, dimensions: Dict[str, str], minutes_ago: int = 30
) -> List[MetricSeries]:
    client = get_datadog_client()
    api_instance = MetricsApi(client)

    now = int(time.time())
    start_time = now - (minutes_ago * 60)

    filter_str = ",".join([f"{k}:{v}" for k, v in dimensions.items()])
    query = f"{metric_name}{{{filter_str}}}"

    response = api_instance.query_timeseries_data(
        body={
            "data": {
                "type": "timeseries_request",
                "attributes": {
                    "queries": [
                        {
                            "data_source": "metrics",
                            "name": "query1",
                            "query": query,
                        }
                    ],
                    "from": start_time * 1000,
                    "to": now * 1000,
                },
            }
        }
    )
    results = []
    if response.data.attributes.series:
        for series in response.data.attributes.series:
            points = [MetricPoint(timestamp=p[0], value=p[1]) for p in series.pointlist]
            results.append(
                MetricSeries(
                    metric_name=series.metric,
                    points=points,
                    tags=dict(tag.split(":", 1) for tag in series.group_tags),
                )
            )
    return results
