from datetime import datetime, timedelta
from typing import Any, Dict

from observability_client import ManagedMetricsClient


def metric_summary(
    project_id: str, metric_name: str, hours: int = 24
) -> Dict[str, Any]:
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    client = ManagedMetricsClient(project_id)
    return client.list_time_series(
        {
            "filter": f'metric.type="{metric_name}"',
            "interval": {
                "startTime": start_time.isoformat() + "Z",
                "endTime": end_time.isoformat() + "Z",
            },
            "view": "FULL",
        }
    )
