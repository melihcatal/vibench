import os
from typing import Any, Dict
from mypy_boto3_logs.client import LogsClient

# Simulated client wrapper for Datadog Logs API - in production this would be the Datadog SDK
# For illustration we use the Datadog Python client (datadog-api-client) which provides `logs` methods.

def get_log_client() -> Any:
    """Returns a configured logging client instance.

    Loads API keys from environment variables. Datadog uses DATADOG_API_KEY and DATADOG_APP_KEY.
    The returned client exposes a `send_log` and a `query_logs` method matching the examples used
    in the scenario files.
    """
    from datadog_api_client.v1.api.logs_api import LogsApi
    from datadog_api_client.v1.configuration import Configuration
    from datadog_api_client.v1.model.log import Log

    api_key = os.getenv("DATADOG_API_KEY")
    app_key = os.getenv("DATADOG_APP_KEY")
    if not api_key or not app_key:
        raise RuntimeError("DATADOG_API_KEY and DATADOG_APP_KEY must be set in the environment")

    configuration = Configuration(api_key=api_key, app_key=app_key)
    return LogsApi(configuration=configuration)

# Example usage within other modules:
# client = get_log_client()
# client.send_log({"event":"test", "value":123})