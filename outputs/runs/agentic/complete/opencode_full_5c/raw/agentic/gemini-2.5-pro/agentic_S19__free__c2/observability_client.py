import os
from datadog_api_client.v2 import ApiClient, ThreadedApiClient
from datadog_api_client.v2.configuration import Configuration


def get_datadog_client() -> ThreadedApiClient:
    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = os.environ.get("DATADOG_API_KEY")
    configuration.api_key["appKeyAuth"] = os.environ.get("DATADOG_APP_KEY")
    configuration.server_variables["site"] = os.environ.get(
        "DATADOG_SITE", "datadoghq.com"
    )

    api_client = ApiClient(configuration)
    return ThreadedApiClient(api_client)
