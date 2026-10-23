
import os
from datetime import datetime, timedelta
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi

def get_metric_summary(metric_name: str, hours_back: int = 24):
    """
    Summarizes recent metric trends or anomalies for a given metric.
    Uses Datadog as the external provider.
    """
    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)

        now = datetime.now()
        start_time = int((now - timedelta(hours=hours_back)).timestamp())
        end_time = int(now.timestamp())

        try:
            # Fetch points for the metric
            response = api_instance.get_metric_data(
                metric_name=metric_name,
                from_=start_time,
                to=end_time
            )

            # Process the response to summarize trends or anomalies
            # This is a placeholder for actual summarization logic
            if response and response.series:
                summary_data = {
                    "metric_name": metric_name,
                    "point_count": sum(len(s.pointlist) for s in response.series),
                    "series_count": len(response.series),
                    "earliest_point": None,
                    "latest_point": None,
                    "avg_value": 0,
                }

                all_values = []
                for series in response.series:
                    for timestamp, value in series.pointlist:
                        all_values.append(value)
                        if summary_data["earliest_point"] is None or timestamp < summary_data["earliest_point"]:
                            summary_data["earliest_point"] = timestamp
                        if summary_data["latest_point"] is None or timestamp > summary_data["latest_point"]:
                            summary_data["latest_point"] = timestamp

                if all_values:
                    summary_data["avg_value"] = sum(all_values) / len(all_values)
                
                return summary_data
            else:
                return {"message": f"No data found for metric '{metric_name}' in the last {hours_back} hours."}

        except Exception as e:
            return {"error": f"Error fetching metric data from Datadog: {e}"}

if __name__ == "__main__":
    # Example usage:
    # Set your Datadog API and Application keys as environment variables
    # DD_API_KEY, DD_APP_KEY
    # For a real application, you'd want to configure these securely.

    metric = "system.cpu.idle" # Replace with the metric you want to summarize
    summary = get_metric_summary(metric)
    print(f"Summary for {metric}: {summary}")
