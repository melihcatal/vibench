from google.cloud import monitoring_v3
from datetime import datetime, timedelta

def compare_metric_series(project_id: str, metric_type: str, filter_str1: str, filter_str2: str, hours: int = 1):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now
    start_time = now - timedelta(hours=hours)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    # Fetch data for the first filter
    query1 = f"""
        fetch gce_instance
        | metric {metric_type}
        | filter {filter_str1}
        | within {start_time.isoformat()}Z, {end_time.isoformat()}Z
        | align rate(1m)
        | every 1m
        | group_by [], [value_mean: mean(value.double_value)]
    """
    results1 = client.query_time_series(name=project_name, query=query1)
    series1_data = []
    for ts in results1.time_series:
        for point in ts.points:
            series1_data.append({
                "timestamp": point.interval.end_time.isoformat(),
                "value": point.value.double_value,
            })

    # Fetch data for the second filter
    query2 = f"""
        fetch gce_instance
        | metric {metric_type}
        | filter {filter_str2}
        | within {start_time.isoformat()}Z, {end_time.isoformat()}Z
        | align rate(1m)
        | every 1m
        | group_by [], [value_mean: mean(value.double_value)]
    """
    results2 = client.query_time_series(name=project_name, query=query2)
    series2_data = []
    for ts in results2.time_series:
        for point in ts.points:
            series2_data.append({
                "timestamp": point.interval.end_time.isoformat(),
                "value": point.value.double_value,
            })

    return {"series1": series1_data, "series2": series2_data}

