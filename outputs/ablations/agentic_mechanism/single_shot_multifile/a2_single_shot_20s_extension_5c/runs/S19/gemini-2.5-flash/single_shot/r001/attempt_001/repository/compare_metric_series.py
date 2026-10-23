import os
from datetime import datetime, timedelta

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi

def compare_metric_series(query_a: str, query_b: str, minutes_ago: int = 60) -> dict:
    configuration = Configuration(
        api_key={'apiKeyAuth': os.environ.get('DATADOG_API_KEY')},
        server_variables={'site': os.environ.get('DATADOG_SITE', 'datadoghq.com')}
    )

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)

        end_time = int(datetime.utcnow().timestamp())
        start_time = int((datetime.utcnow() - timedelta(minutes=minutes_ago)).timestamp())

        response_a = api_instance.query_metrics(
            query=query_a,
            _from=start_time,
            to=end_time,
        )

        response_b = api_instance.query_metrics(
            query=query_b,
            _from=start_time,
            to=end_time,
        )

        return {
            "series_a": response_a.to_dict(),
            "series_b": response_b.to_dict()
        }