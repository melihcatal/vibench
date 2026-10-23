from datetime import datetime, timedelta
import os

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.logs_api import LogsApi
from datadog_api_client.v1.model.log_query_definition import LogQueryDefinition
from datadog_api_client.v1.model.logs_list_request import LogsListRequest
from datadog_api_client.v1.model.logs_list_request_time import LogsListRequestTime
from datadog_api_client.v1.model.logs_sort import LogsSort


def fetch_recent_logs(query: str = None, hours: int = 1):
    """
    Retrieves recent log results from Datadog filtered by field values and time range.

    Args:
        query (str): The log query string to filter results (e.g., "status:error service:my-app").
        hours (int): The number of hours to look back for logs.
    """
    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = LogsApi(api_client)

        now = datetime.now()
        start_time = now - timedelta(hours=hours)

        # Datadog API expects timestamps in milliseconds
        start_timestamp_ms = int(start_time.timestamp() * 1000)
        end_timestamp_ms = int(now.timestamp() * 1000)

        body = LogsListRequest(
            query=query,
            sort=LogsSort("desc"),  # Or "asc"
            time=LogsListRequestTime(
                _from=start_timestamp_ms,
                to=end_timestamp_ms,
            ),
        )

        try:
            response = api_instance.list_logs(body=body)
            for log in response.data:
                print(log.content)
        except Exception as e:
            print(f"Error fetching logs: {e}")


if __name__ == "__main__":
    # Ensure DATADOG_API_KEY and DATADOG_APP_KEY are set in your environment
    if "DATADOG_API_KEY" not in os.environ or "DATADOG_APP_KEY" not in os.environ:
        print("Please set DATADOG_API_KEY and DATADOG_APP_KEY environment variables.")
    else:
        # Example usage: Fetch logs with "error" in the message from the last 2 hours
        fetch_recent_logs(query="status:error", hours=2)
