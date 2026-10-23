import os
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem

def get_logging_client():
    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = os.getenv("DD_API_KEY")
    configuration.api_key["appKeyAuth"] = os.getenv("DD_APP_KEY")
    
    if not configuration.api_key["apiKeyAuth"] or not configuration.api_key["appKeyAuth"]:
        raise ValueError("Datadog API and App keys must be set in environment variables.")
    
    return LogsApi(ApiClient(configuration))