import time
from typing import Optional
from datadog_api_client.v2.api.metrics_api import MetricsApi
from observability_client import get_datadog_client
from observability_models import MetricStatistics


def get_aggregate_stats(
    metric_name: str, minutes_ago: int = 60
) -> Optional[MetricStatistics]:
    client = get_datadog_client()
    api_instance = MetricsApi(client)

    now = int(time.time())
    start_time = now - (minutes_ago * 60)

    response = api_instance.query_scalar_data(
        body={
            "data": {
                "type": "scalar_request",
                "attributes": {
                    "queries": [
                        {
                            "data_source": "metrics",
                            "name": "query1",
                            "query": f"avg:{metric_name}{{*}}.as_count()",
                            "aggregator": "sum",
                        },
                        {
                            "data_source": "metrics",
                            "name": "query2",
                            "query": f"min:{metric_name}{{*}}.as_count()",
                            "aggregator": "min",
                        },
                        {
                            "data_source": "metrics",
                            "name": "query3",
                            "query": f"max:{metric_name}{{*}}.as_count()",
                            "aggregator": "max",
                        },
                        {
                            "data_source": "metrics",
                            "name": "query4",
                            "query": f"sum:{metric_name}{{*}}.as_count()",
                            "aggregator": "sum",
                        },
                    ],
                    "from": start_time * 1000,
                    "to": now * 1000,
                },
            }
        }
    )

    if not response.data or not response.data.attributes.columns:
        return None

    # This assumes a single group response for simplicity
    row = response.data.attributes.rows[0]

    return MetricStatistics(
        metric_name=metric_name,
        avg=row[0],
        min=row[1],
        max=row[2],
        sum=row[3],
    )
