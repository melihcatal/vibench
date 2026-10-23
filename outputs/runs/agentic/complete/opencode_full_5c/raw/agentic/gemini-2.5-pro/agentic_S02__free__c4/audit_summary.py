from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_sort import LogsSort

from identity_client import get_identity_config


def get_federated_login_summary():
    config = get_identity_config()

    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = config.DATADOG_API_KEY
    configuration.api_key["appKeyAuth"] = config.DATADOG_APP_KEY

    with ApiClient(configuration) as api_client:
        api_instance = LogsApi(api_client)

        body = LogsListRequest(
            filter=LogsQueryFilter(
                query="source:python @event_type:login_success",
                _from="now-1d",
                to="now",
            ),
            sort=LogsSort.TIMESTAMP_DESCENDING,
            page=None,
        )

        try:
            api_response = api_instance.list_logs(body)
            return api_response
        except Exception as e:
            print(f"Exception when calling LogsApi->list_logs: {e}")
            return None


if __name__ == "__main__":
    # This is for verification, not example usage
    summary = get_federated_login_summary()
    if summary:
        print("Successfully fetched audit summary from Datadog.")
        print(f"Found {len(summary.data)} events in the last day.")
        for event in summary.data:
            print(event.attributes.message)
    else:
        print("Failed to fetch audit summary from Datadog.")
