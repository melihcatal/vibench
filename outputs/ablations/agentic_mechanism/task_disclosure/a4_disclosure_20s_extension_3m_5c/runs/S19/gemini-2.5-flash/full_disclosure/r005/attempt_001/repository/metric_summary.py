
from google.cloud import monitoring_v3
from google.protobuf.duration_pb2 import Duration
from datetime import datetime, timedelta

def summarize_metric_trends(project_id: str, metric_type: str, minutes_ago: int = 60):
    """
    Summarizes recent metric trends or anomalies using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/usage_time").
        minutes_ago: The number of minutes from now to query metric data.
    
    Returns:
        A dictionary containing a summary of the metric, or an error message.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.now()
    end_time = now
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time.timestamp())},
        start_time={'seconds': int(start_time.timestamp())}
    )

    query = f"fetch_time_series_data | {metric_type}"
    
    try:
        response = client.query_time_series(
            name=project_name,
            query=query,
            time_interval=interval
        )

        if not response.time_series_data:
            return {"summary": "No data found for the specified metric and time window."}

        # Basic summarization: get min, max, and average of all points
        all_values = []
        for time_series_data in response.time_series_data:
            for point in time_series_data.point_data:
                if point.values:
                    # Assuming the value type is double, adjust if different
                    all_values.append(point.values[0].double_value)

        if not all_values:
            return {"summary": "No valid data points to summarize."}

        min_value = min(all_values)
        max_value = max(all_values)
        avg_value = sum(all_values) / len(all_values)

        return {
            "metric_type": metric_type,
            "time_window_minutes": minutes_ago,
            "min_value": min_value,
            "max_value": max_value,
            "average_value": avg_value,
            "num_data_points": len(all_values)
        }

    except Exception as e:
        return {"error": f"An error occurred: {e}"}

