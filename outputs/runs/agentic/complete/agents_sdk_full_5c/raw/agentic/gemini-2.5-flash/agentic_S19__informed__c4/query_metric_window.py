from google.cloud import monitoring_v3
from datetime import datetime, timedelta

def query_metric_window(project_id: str, metric_type: str, hours: int = 1):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now
    start_time = now - timedelta(hours=hours)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    query = f"""
        fetch gce_instance
        | metric {metric_type}
        | within {start_time.isoformat()}Z, {end_time.isoformat()}Z
        | align rate(1m)
        | every 1m
        | group_by [], [value_mean: mean(value.double_value)]
    """

    results = client.query_time_series(
        name=project_name,
        query=query,
    )
    
    time_series_data = []
    for ts in results.time_series:
        for point in ts.points:
            time_series_data.append({
                "timestamp": point.interval.end_time.isoformat(),
                "value": point.value.double_value
            })
    return time_series_data

