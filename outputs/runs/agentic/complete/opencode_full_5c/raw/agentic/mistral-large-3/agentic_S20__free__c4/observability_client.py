import os
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi


def get_logging_client():
    """
    Initializes and returns a Datadog logging client.

    Returns:
        Datadog LogsApi client for log ingestion and querying.
    """
    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = os.getenv("DATADOG_API_KEY")
    configuration.api_key["appKeyAuth"] = os.getenv("DATADOG_APPLICATION_KEY")

    if (
        not configuration.api_key["apiKeyAuth"]
        or not configuration.api_key["appKeyAuth"]
    ):
        raise ValueError(
            "Datadog API key or Application key not set in environment variables."
        )

    api_client = ApiClient(configuration)
    return LogsApi(api_client)
