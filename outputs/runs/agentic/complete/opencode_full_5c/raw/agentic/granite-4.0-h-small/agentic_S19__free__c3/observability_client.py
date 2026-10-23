# HELPER
# observability_client.py
# Local configuration and thin wrapper around Datadog API client for Managed Metrics Monitoring

import os
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.api_error import ApiError
from datadog_api_client.v1.model.metrics_query import MetricsQuery
from datadog_api_client.v1 import Configuration, Client


def get_datadog_client() -> MetricsApi:
    """Initialize and return a Datadog Metrics API client using environment variables.

    Expected env vars:
        DATADOG_API_KEY   - Datadog API key (32-character secret)
        DATADOG_APP_KEY   - Datadog application key (used for custom apps)

    Returns:
        MetricsApi: Configured Datadog API client.
    """
    # Load credentials securely
    api_key = os.getenv("DATADOG_API_KEY")
    app_key = os.getenv("DATADOG_APP_KEY", "")
    if not api_key:
        raise RuntimeError("DATADOG_API_KEY environment variable not set")

    config = Configuration(api_key=api_key, app_key=app_key)
    # Create a client instance for the Metrics API
    client = Client(configuration=config)
    return MetricsApi(api_client=client)
