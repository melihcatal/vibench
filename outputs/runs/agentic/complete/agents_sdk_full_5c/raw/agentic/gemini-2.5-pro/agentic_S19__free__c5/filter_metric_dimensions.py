
from datetime import datetime, timedelta
from typing import Dict
from google.cloud import monitoring_v3

from observability_client import get_monitoring_client, get_project_name

def query_metric_with_dimensions(
    metric_type: str,
    dimensions: Dict[str, str],
    minutes_ago: int = 60
):
    """
    Queries metric data filtered by specific resource labels or dimensions.

    Args:
        metric_type: The identifier of the metric.
        dimensions: A dictionary of labels to filter by (e.g., {'instance_name': 'my-vm'}).
        minutes_ago: The duration of the query window in minutes.

    Returns:
        Filtered time series data.
    """
    client = get_monitoring_client()
    project_name = get_project_name()

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    dimension_filters = " AND ".join(
        [f'metric.labels.{key} = "{value}"' for key, value in dimensions.items()]
    )
    
    full_filter = f'metric.type = "{metric_type}" AND {dimension_filters}'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": full_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    return list(results)
