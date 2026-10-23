import os
from datetime import datetime, timedelta
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_query_response import MetricsQueryResponse
from datadog_api_client.exceptions import ApiException
from datadog_api_client.configuration import Configuration

def get_datadog_metrics(query: str, start_time: datetime, end_time: datetime) -> MetricsQueryResponse | None:
    """
    Fetches metric data from Datadog.
    """
    configuration = Configuration()
    configuration.api_key["app_key"] = os.getenv("DATADOG_APPLICATION_KEY", "YOUR_DATADOG_APP_KEY")
    configuration.api_key["api_key"] = os.getenv("DATADOG_API_KEY", "YOUR_DATADOG_API_KEY")

    api_instance = MetricsApi(configuration)

    try:
        response = api_instance.query_metrics(
            _from=int(start_time.timestamp()),
            to=int(end_time.timestamp()),
            query=query,
        )
        return response
    except ApiException as e:
        print(f"Error fetching metrics from Datadog: {e}")
        return None

def summarize_metrics(metric_name: str, days: int = 7):
    """
    Summarizes recent metric trends or anomalies for a given metric.
    """
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)

    query = f"avg:{metric_name}{{host:my-host}}.rollup(avg, 3600)" # Example query, replace with actual metric and scope

    print(f"Fetching data for metric: {metric_name} from {start_time} to {end_time}")
    metrics_data = get_datadog_metrics(query, start_time, end_time)

    if metrics_data and metrics_data.series:
        print(f"Successfully fetched {len(metrics_data.series[0].pointlist)} data points for {metric_name}.")
        # Basic trend analysis (for demonstration purposes)
        if len(metrics_data.series[0].pointlist) > 1:
            first_value = metrics_data.series[0].pointlist[0][1]
            last_value = metrics_data.series[0].pointlist[-1][1]
            if first_value is not None and last_value is not None:
                if last_value > first_value * 1.1:
                    print(f"Anomaly detected: {metric_name} has increased by more than 10% over the last {days} days.")
                elif last_value < first_value * 0.9:
                    print(f"Anomaly detected: {metric_name} has decreased by more than 10% over the last {days} days.")
                else:
                    print(f"Trend for {metric_name}: Relatively stable over the last {days} days.")
            else:
                print(f"Could not determine trend for {metric_name} due to missing data points.")
        else:
            print(f"Not enough data points to determine a trend for {metric_name}.")
    else:
        print(f"No metric data found for {metric_name} or an error occurred.")

if __name__ == "__main__":
    # Example usage
    # Ensure to set DATADOG_API_KEY and DATADOG_APPLICATION_KEY environment variables
    # or replace "YOUR_DATADOG_APP_KEY" and "YOUR_DATADOG_API_KEY" with actual keys.
    metric_to_summarize = "system.cpu.idle" # Replace with a real Datadog metric
    summarize_metrics(metric_to_summarize, days=7)
