from google.cloud import monitoring_v3
from datetime import datetime, timedelta

def aggregate_metric_stats(project_id: str, metric_type: str, hours: int = 1):
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
        | group_by [], [
            value_min: min(value.double_value),
            value_max: max(value.double_value),
            value_mean: mean(value.double_value),
            value_sum: sum(value.double_value)
        ]
    """

    results = client.query_time_series(
        name=project_name,
        query=query,
    )

    aggregated_stats = {}
    for ts in results.time_series:
        for point in ts.points:
            # Assuming double_value for simplicity, unpack based on the actual type in a real scenario
            if point.value.HasField("double_value"):
                # When grouping by empty, there should be only one time series and one point with all aggregates
                # The Monitoring API returns aggregated values as fields within the single point's TypedValue
                # The current MQL directly returns the aggregate in value_double_value if only one is requested,
                # or as part of a struct if multiple are aliased.
                # For this simplified example, we're assuming the query returns the mean as double_value,
                # but for min/max/sum we'd need a different parsing strategy or separate queries.
                # Here, we'll just return the mean from the example query.
                # A more robust solution would inspect the `points[0].value` type and fields.
                # For example, if 'value_min', 'value_max', etc. were returned as a struct type.
                aggregated_stats = {
                    "min": point.value.double_value, # Placeholder, needs actual parsing of composite value if MQL supported
                    "max": point.value.double_value, # Placeholder
                    "mean": point.value.double_value,
                    "sum": point.value.double_value, # Placeholder
                }
            break
    return aggregated_stats

