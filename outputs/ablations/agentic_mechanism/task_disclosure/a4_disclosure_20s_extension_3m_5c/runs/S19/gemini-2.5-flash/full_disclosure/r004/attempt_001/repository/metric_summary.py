from google.cloud import monitoring_v3
from datetime import datetime, timedelta

def summarize_metric_trends(project_id: str, metric_type: str, minutes: int = 60):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    start_time = (now - timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")

    query = f"""
        fetch {metric_type.split("/")[0]}
        | metric {metric_type}
        | group_by [], [value_mean: mean(value)]
        | within d'{start_time}', d'{end_time}'
    """

    try:
        response = client.query_time_series(
            request={
                "name": project_name,
                "query": query,
            }
        )

        summary_data = []
        for time_series in response.time_series_data:
            for point in time_series.points:
                summary_data.append({
                    "timestamp": point.interval.end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "value": point.value.double_value
                })
        
        # Placeholder for actual trend/anomaly summarization logic
        if summary_data:
            return f"Successfully retrieved {len(summary_data)} data points for metric {metric_type}. Further analysis would summarize trends or anomalies."
        else:
            return f"No data found for metric {metric_type} in the last {minutes} minutes."

    except Exception as e:
        return f"Error summarizing metric trends: {e}