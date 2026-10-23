
import os
from datetime import datetime, timedelta
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi

# Configuration
# Set your Datadog API key and APP key as environment variables
# DD_API_KEY and DD_APPLICATION_KEY
api_key = os.getenv("DD_API_KEY")
app_key = os.getenv("DD_APPLICATION_KEY")

if not api_key or not app_key:
    raise ValueError("Datadog API key (DD_API_KEY) and Application key (DD_APPLICATION_KEY) must be set as environment variables.")

configuration = Configuration(
    api_key={"apiKeyAuth": api_key},
    app_key={"appKeyAuth": app_key},
)

def query_metric_window(metric_name: str, hours_ago: int = 1, interval_seconds: int = 60):
    """
    Queries recent datapoints for a named metric over a time window using Datadog.

    Args:
        metric_name (str): The name of the metric to query (e.g., "system.cpu.idle").
        hours_ago (int): The number of hours back from now to query.
        interval_seconds (int): The interval between datapoints in seconds.
    """
    now = datetime.now()
    end_time = int(now.timestamp())
    start_time = int((now - timedelta(hours=hours_ago)).timestamp())

    query_string = f"avg:{metric_name}{{*}_by_host" # Example query, aggregates by host

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        try:
            response = api_instance.query_metrics(
                _from=start_time,
                to=end_time,
                query=query_string
            )
            print(f"Datadog Metric Query Response for {metric_name}:")
            if response and response.get("series"):
                for series in response["series"]:
                    print(f"  Metric: {series.get("metric")}, Scope: {series.get("scope")}")
                    for point in series["pointlist"]:
                        timestamp = datetime.fromtimestamp(point[0] / 1000) # Datadog returns ms
                        value = point[1]
                        print(f"    Timestamp: {timestamp}, Value: {value}")
            else:
                print("  No data found for the specified metric and time window.")

        except Exception as e:
            print(f"Error querying Datadog metric: {e}")

if __name__ == "__main__":
    # Example usage:
    # Make sure to set DD_API_KEY and DD_APPLICATION_KEY environment variables
    # For example:
    # export DD_API_KEY="your_datadog_api_key"
    # export DD_APPLICATION_KEY="your_datadog_application_key"
    #
    # To run: python query_metric_window.py
    # or python -c "from query_metric_window import query_metric_window; query_metric_window('system.cpu.idle', hours_ago=2)"

    # Replace 'system.cpu.idle' with the actual metric you want to query
    query_metric_window("system.cpu.idle", hours_ago=1)
