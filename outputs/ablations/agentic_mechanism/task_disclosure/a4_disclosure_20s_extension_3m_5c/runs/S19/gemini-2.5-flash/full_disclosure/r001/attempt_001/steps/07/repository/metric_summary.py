
from google.cloud import monitoring_v3
from google.protobuf.duration_pb2 import Duration
from datetime import datetime, timedelta

def summarize_metric_trends(project_id: str, metric_type: str, minutes_ago: int = 60):
    """
    Summarizes recent metric trends or anomalies using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud Project ID.
        metric_type: The full metric type (e.g., "agent.googleapis.com/memory/bytes_used").
        minutes_ago: The number of minutes in the past to retrieve data for.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now
    start_time = now - timedelta(minutes=minutes_ago)

    # Convert to RFC3339 format
    end_time_str = end_time.isoformat("T") + "Z"
    start_time_str = start_time.isoformat("T") + "Z"

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time.timestamp())},
        start_time={'seconds': int(start_time.timestamp())}
    )

    query = f"""
        fetchTimeSeries(
            {metric_type},
            metric.labels.instance_name = starts_with("my-instance")
        )
        | within(P{minutes_ago}M)
        | group_by(
            [metric.instance_name],
            [value_mean: mean(value)]
        )
    """

    results = client.query_time_series(
        request={
            "name": project_name,
            "query": query,
        }
    )

    summary = []
    for time_series in results.time_series_data:
        # Assuming the query returns aggregated data with one point per series
        if time_series.point_data:
            point = time_series.point_data[0]
            instance_name = None
            for label, value in time_series.label_values.items():
                if label == "instance_name":
                    instance_name = value.string_value
                    break
            
            if instance_name:
                summary.append(f"Instance: {instance_name}, Mean Value: {point.values[0].double_value}")
            else:
                summary.append(f"Mean Value: {point.values[0].double_value}")

    return summary

