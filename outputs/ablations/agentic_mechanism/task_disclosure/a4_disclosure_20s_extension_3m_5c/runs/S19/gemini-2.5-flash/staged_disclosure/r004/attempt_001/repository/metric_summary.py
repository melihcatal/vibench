
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datetime import datetime, timedelta
import os

# Configure Datadog API client
configuration = Configuration()
configuration.api_key["app_key"] = os.getenv("DATADOG_APPLICATION_KEY")
configuration.api_key["api_key"] = os.getenv("DATADOG_API_KEY")

def summarize_metrics(query: str, days: int = 7):
    """
    Summarizes recent metric trends or anomalies using Datadog.

    Args:
        query (str): The Datadog metric query (e.g., "avg:system.cpu.idle{*}").
        days (int): The number of past days to fetch data for.

    Returns:
        dict: A dictionary containing the metric summary.
    """
    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)

        now = datetime.now()
        end_time = int(now.timestamp())
        start_time = int((now - timedelta(days=days)).timestamp())

        try:
            response = api_instance.query_metrics(
                query=query,
                from_=start_time,
                to=end_time,
            )
            
            # Process the response to summarize trends/anomalies
            # This is a basic example; more sophisticated analysis would be needed
            # for real-world anomaly detection or trend summarization.
            
            summary = {
                "query": query,
                "start_time": datetime.fromtimestamp(start_time).isoformat(),
                "end_time": datetime.fromtimestamp(end_time).isoformat(),
                "data_points_count": 0,
                "avg_value": None,
                "metric_series": []
            }

            if response and response.series:
                all_points = []
                for series in response.series:
                    summary["metric_series"].append({
                        "metric": series.metric,
                        "scope": series.scope,
                        "display_name": series.display_name,
                        "unit": series.unit,
                        "pointlist_count": len(series.pointlist)
                    })
                    for point_time, point_value in series.pointlist:
                        if point_value is not None:
                            all_points.append(point_value)
                
                if all_points:
                    summary["data_points_count"] = len(all_points)
                    summary["avg_value"] = sum(all_points) / len(all_points)
            
            return summary

        except Exception as e:
            return {"error": str(e)}

# Example usage (uncomment to test, ensure DATADOG_API_KEY and DATADOG_APPLICATION_KEY are set as environment variables)
# if __name__ == "__main__":
#     metric_query = "avg:system.cpu.idle{*} by {host}"
#     summary = summarize_metrics(metric_query, days=1)
#     print(summary)
