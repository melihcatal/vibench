import os
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi

def get_logging_client():
    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = os.getenv("DATADOG_API_KEY")
    configuration.api_key["appKeyAuth"] = os.getenv("DATADOG_APP_KEY")
    configuration.server_variables["site"] = os.getenv("DATADOG_SITE", "datadoghq.com")
    return LogsApi(ApiClient(configuration))