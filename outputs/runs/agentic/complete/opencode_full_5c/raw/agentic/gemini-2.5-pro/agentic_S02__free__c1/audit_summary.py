from datadog_api_client.v2 import ApiClient, ApiException
from datadog_api_client.v2.api import logs_api
from datadog_api_client.v2.models import LogsListRequest, LogsQueryFilter, LogsSort

from identity_client import IdentityClientConfig


def get_login_audit_summary():
    config = IdentityClientConfig()

    configuration = ApiClient.configuration
    configuration.api_key["apiKeyAuth"] = config.DATADOG_API_KEY
    configuration.api_key["appKeyAuth"] = config.DATADOG_APP_KEY

    with ApiClient(configuration) as api_client:
        api_instance = logs_api.LogsApi(api_client)

        body = LogsListRequest(
            filter=LogsQueryFilter(
                query="source:python @evt.name:federated_login",
                _from="now-1d",
                to="now",
            ),
            sort=LogsSort.TIMESTAMP_DESCENDING,
        )

        try:
            api_response = api_instance.list_logs(body)
            return api_response
        except ApiException as e:
            print(f"Exception when calling LogsApi->list_logs: {e}\n")
            return None
