import time
from typing import List
from datadog_api_client.v2.api.metrics_api import MetricsApi
from observability_client import get_datadog_client
from observability_models import MetricSeries, MetricPoint


def query_recent_metrics(metric_name: str, minutes_ago: int = 15) -> List[MetricSeries]:
    client = get_datadog_client()
    api_instance = MetricsApi(client)

    now = int(time.time())
    start_time = now - (minutes_ago * 60)

    response = api_instance.query_timeseries_data(
        body={
            "data": {
                "type": "timeseries_request",
                "attributes": {
                    "queries": [
                        {
                            "data_source": "metrics",
                            "name": "query1",
                            "query": f"{metric_name}{{*}}",
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
            results.append(MetricSeries(metric_name=series.metric, points=points))
    return results
