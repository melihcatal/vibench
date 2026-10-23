import os
from datadog_api_client.v2 import ApiClient, ApiException
from datadog_api_client.v2.api import metrics_api
from datadog_api_client.v2.models import MetricSeries, MetricPoint, MetricIntakeType

def summarize_logins_to_datadog(provider: str, success_count: int, failure_count: int):
    """
    Submits summary metrics of federated logins to Datadog.

    Args:
        provider (str): The identity provider (e.g., 'okta').
        success_count (int): The number of successful logins.
        failure_count (int): The number of failed logins.
    """
    
    if not os.environ.get("DD_API_KEY") or not os.environ.get("DD_SITE"):
        raise ValueError("DD_API_KEY and DD_SITE environment variables must be set.")

    configuration = ApiClient.configuration
    with ApiClient(configuration) as api_client:
        api_instance = metrics_api.MetricsApi(api_client)
        
        current_timestamp = int(datetime.datetime.now().timestamp())
        
        series = [
            MetricSeries(
                metric="federated_login.summary.success",
                type=MetricIntakeType.COUNT,
                points=[MetricPoint(timestamp=current_timestamp, value=float(success_count))],
                tags=[f"provider:{provider}"],
            ),
            MetricSeries(
                metric="federated_login.summary.failure",
                type=MetricIntakeType.COUNT,
                points=[MetricPoint(timestamp=current_timestamp, value=float(failure_count))],
                tags=[f"provider:{provider}"],
            ),
        ]
        
        body = {"series": series}

        try:
            api_response = api_instance.submit_metrics(body=body)
            print(f"Successfully submitted metrics to Datadog: {api_response}")
        except ApiException as e:
            print(f"Error when calling MetricsApi->submit_metrics: {e}")

# This function would typically be called by a background job
# that queries and aggregates data from an audit store.
import datetime
