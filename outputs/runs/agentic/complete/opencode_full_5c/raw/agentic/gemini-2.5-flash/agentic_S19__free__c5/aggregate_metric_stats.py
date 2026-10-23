import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3


def aggregate_metric_stats(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    minutes: int = 60,
    agg_function: str = "mean",
):
    """Retrieves aggregated statistics for a metric over a time window."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    query = (
        f'fetchTimeSeries({project_name}, "metric.type="{metric_type}"")'
        f' | within(start_time="{start_time.isoformat()}Z", end_time="{end_time.isoformat()}Z")'
        f" | {agg_function}()"
    )

    results = client.query_time_series(
        name=project_name,
        query=query,
    )

    return results
