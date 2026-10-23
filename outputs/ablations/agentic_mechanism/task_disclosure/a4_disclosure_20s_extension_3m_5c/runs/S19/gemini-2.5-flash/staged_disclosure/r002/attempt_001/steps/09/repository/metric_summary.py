
import os
from datetime import datetime, timedelta
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi

def get_metric_trends(metric_name: str, hours: int = 1):
    """
    Fetches recent metric data from Datadog and provides a summary.
    """
    api_key = os.getenv("DD_API_KEY")
    app_key = os.getenv("DD_APP_KEY")

    if not api_key or not app_key:
        return "Datadog API keys not found. Please set DD_API_KEY and DD_APP_KEY environment variables."

    configuration = Configuration(
        api_key={"apiKeyAuth": api_key, "appKeyAuth": app_key}
    )

    with ApiClient(configuration) as api_client:
        metrics_api = MetricsApi(api_client)

        now = datetime.now()
        end_time = int(now.timestamp())
        start_time = int((now - timedelta(hours=hours)).timestamp())

        try:
            response = metrics_api.query_metrics(
                _from=start_time,
                to=end_time,
                query=f"avg:{metric_name}{{*} by {{host}}" # Example query
            )
            
            if response and response.get("series"):
                summary = f"Metric: {metric_name} trends over the last {hours} hour(s):
"
                for series in response["series"]:
                    scope = series.get("scope", "N/A")
                    points = series.get("pointlist", [])
                    if points:
                        latest_value = points[-1][1] if points[-1][1] is not None else "N/A"
                        summary += f"  - Host/Scope: {scope}, Latest Value: {latest_value}
"
                return summary
            else:
                return f"No data found for metric '{metric_name}' in the last {hours} hour(s)."

        except Exception as e:
            return f"Error fetching metric from Datadog: {e}"

if __name__ == "__main__":
    # Example usage:
    # Set your Datadog API and Application keys as environment variables:
    # export DD_API_KEY="YOUR_DATADOG_API_KEY"
    # export DD_APP_KEY="YOUR_DATADOG_APP_KEY"
    
    # Replace 'system.cpu.idle' with the actual metric you want to monitor
    print(get_metric_trends("system.cpu.idle", hours=1))
