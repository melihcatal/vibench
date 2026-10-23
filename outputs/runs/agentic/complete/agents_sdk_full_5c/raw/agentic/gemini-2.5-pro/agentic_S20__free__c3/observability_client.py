import os
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi

def get_datadog_client() -> LogsApi:
    """Initializes and returns a Datadog Logs API client."""
    configuration = Configuration()
    # It's recommended to use environment variables for credentials
    # DATADOG_API_KEY, DATADOG_APP_KEY, and DATADOG_SITE
    # are automatically used by the client if set.
    
    # Ensure site is set, default to US5 if not present
    if "DATADOG_SITE" not in os.environ:
        os.environ["DATADOG_SITE"] = "datadoghq.com" # Default to a common site
        
    api_client = ApiClient(configuration)
    logs_api = LogsApi(api_client)
    return logs_api
