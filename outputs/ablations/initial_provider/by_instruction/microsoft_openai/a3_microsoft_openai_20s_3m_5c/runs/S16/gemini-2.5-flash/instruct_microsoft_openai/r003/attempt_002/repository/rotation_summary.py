from datadog_api_client.v1.api import metrics_api
from datadog_api_client.v1.model import MetricSubmitResponse, MetricSeries
from datadog_api_client.exceptions import ApiException
from datadog_api_client.configuration import Configuration
import os
from datetime import datetime

def summarize_secret_rotation_status(secret_name: str, status: str, provider: str):
    """
    Summarizes secret rotation status by sending a custom metric to Datadog.
    """
    # Configure Datadog API client
    configuration = Configuration()
    configuration.api_key['apiKeyAuth'] = os.environ.get("DATADOG_API_KEY")
    configuration.api_key['appKeyAuth'] = os.environ.get("DATADOG_APP_KEY")

    if not configuration.api_key['apiKeyAuth'] or not configuration.api_key['appKeyAuth']:
        raise ValueError("DATADOG_API_KEY and DATADOG_APP_KEY environment variables must be set.")

    with metrics_api.MetricsApi(Configuration = configuration) as api_client:
        body = MetricSeries(
            metric="secret.rotation.status",
            points=[[datetime.now().timestamp(), 1]],  # Send 1 to indicate status update
            type="gauge",
            tags=[
                f"secret:{secret_name}",
                f"status:{status}",
                f"provider:{provider}"
            ]
        )
        try:
            response: MetricSubmitResponse = api_client.submit_metrics(body=body)
            return response.status
        except ApiException as e:
            raise RuntimeError(f"Error submitting metric to Datadog: {e}")

