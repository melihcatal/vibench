import os
from datetime import datetime, timedelta
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi

# Datadog API keys - Replace with your actual keys or set as environment variables
DD_API_KEY = os.getenv("DD_API_KEY", "YOUR_DATADOG_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY", "YOUR_DATADOG_APP_KEY")

if DD_API_KEY == "YOUR_DATADOG_API_KEY" or DD_APP_KEY == "YOUR_DATADOG_APP_KEY":
    print("Please set your Datadog API and Application keys either as environment variables (DD_API_KEY, DD_APP_KEY) or directly in the script.")
    exit(1)

configuration = Configuration()
configuration.api_key["app_key"] = DD_APP_KEY
configuration.api_key["api_key"] = DD_API_KEY

def summarize_metrics(query: str, time_window_minutes: int = 60):
    """
    Summarizes recent metric trends or anomalies from Datadog.

    Args:
        query (str): The Datadog metric query string (e.g., "avg:system.cpu.idle{*}").
        time_window_minutes (int): The time window in minutes to fetch metrics for.
    """
    now = datetime.now()
    end_time = int(now.timestamp())
    start_time = int((now - timedelta(minutes=time_window_minutes)).timestamp())

    try:
        with ApiClient(configuration) as api_client:
            api_instance = MetricsApi(api_client)
            response = api_instance.query_metrics(
                query=query,
                from_=start_time,
                to=end_time,
            )

            if response and response.series:
                print(f"Metric Summary for query: '{query}' over the last {time_window_minutes} minutes:")
                for series in response.series:
                    points = [point[1] for point in series.pointlist if point[1] is not None]
                    if points:
                        avg_value = sum(points) / len(points)
                        max_value = max(points)
                        min_value = min(points)
                        print(f"  Metric: {series.display_name}")
                        print(f"    Average: {avg_value:.2f}")
                        print(f"    Maximum: {max_value:.2f}")
                        print(f"    Minimum: {min_value:.2f}")
                        print(f"    Data points: {len(points)}")
                    else:
                        print(f"  No data points found for metric: {series.display_name}")
            else:
                print(f"No metric data found for query: '{query}'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage:
    # Replace with your desired metric query
    # You can find metric queries in your Datadog dashboard
    # For example, "avg:system.cpu.user{host:my-host}" or "sum:aws.ec2.cpuutilization{*}by{region}"
    metric_to_summarize = "avg:system.cpu.idle{*}"
    time_window = 30 # minutes

    print("Attempting to summarize metrics...")
    summarize_metrics(metric_to_summarize, time_window)
