from datadog_api_client.v2 import ApiClient, ApiException
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.models import LogsListRequest, LogsQueryFilter
import os
from datetime import datetime, timedelta


def get_login_summary():
    """
    Summarizes federated-login audit events from Datadog.
    """
    configuration = ApiClient.configuration
    configuration.api_key["apiKeyAuth"] = os.environ.get("DATADOG_API_KEY")
    configuration.api_key["appKeyAuth"] = os.environ.get("DATADOG_APP_KEY")

    api_instance = LogsApi(ApiClient(configuration))

    now = datetime.now()
    twenty_four_hours_ago = now - timedelta(hours=24)

    try:
        response = api_instance.list_logs(
            body=LogsListRequest(
                filter=LogsQueryFilter(
                    query="source:python @evt.name:federated_login",
                    _from=twenty_four_hours_ago.isoformat() + "Z",
                    to=now.isoformat() + "Z",
                )
            )
        )

        summary = {
            "total_logins": len(response.data),
            "logins": [log.attributes.attributes for log in response.data],
        }
        return summary
    except ApiException as e:
        print(f"Exception when calling LogsApi->list_logs: {e}\n")
        return None


# Required environment variables:
# export DATADOG_API_KEY="your_api_key"
# export DATADOG_APP_KEY="your_app_key"
