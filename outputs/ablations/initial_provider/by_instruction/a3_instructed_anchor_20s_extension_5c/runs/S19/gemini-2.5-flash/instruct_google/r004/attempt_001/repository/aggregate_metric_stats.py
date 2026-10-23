from google.cloud import monitoring_v3
from datetime import datetime, timedelta

def aggregate_metric_stats(project_id: str, metric_type: str, minutes_ago: int = 60, reducer: str = "REDUCE_MEAN"):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    # Construct the query with aggregation
    # Note: Google Cloud Monitoring's MQL is very powerful for aggregation.
    # For simplicity, this example fetches time series and then applies a reducer in code
    # or assumes a simple aggregation if supported directly by a basic filter.
    # A more complex MQL query would be needed for advanced server-side aggregation.

    # For this example, we will fetch raw data and demonstrate a simple mean calculation
    # A real-world scenario might use MQL directly for server-side aggregation.
    query = f"fetch gce_instance | metric {metric_type}"

    results = client.query_time_series(
        name=project_name,
        query=query,
        interval=interval,
        # This part would be more complex with aggregation. For now, just fetching data.
    )

    all_values = []
    for time_series in results:
        for point in time_series.points:
            all_values.append(point.value.double_value)

    if not all_values:
        return {"metric_type": metric_type, "aggregation_type": reducer, "value": None}

    # Simple aggregation in Python for demonstration. In a real scenario, use MQL's aligner and reducer.
    if reducer == "REDUCE_MEAN":
        aggregated_value = sum(all_values) / len(all_values)
    elif reducer == "REDUCE_MAX":
        aggregated_value = max(all_values)
    elif reducer == "REDUCE_MIN":
        aggregated_value = min(all_values)
    else:
        aggregated_value = None # Or raise an error for unsupported reducer

    return {"metric_type": metric_type, "aggregation_type": reducer, "value": aggregated_value}
