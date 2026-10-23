from datetime import datetime, timedelta
import os
from google.cloud import monitoring_v3
from observability_client import get_client_config
from observability_models import MetricSummaryRequest


def detect_anomalies(values: list[float], threshold: float) -> list[bool]:
    """Detect anomalies in metric values using a simple threshold check."""
    return [value > threshold for value in values]


def summarize_metric_trends(request: MetricSummaryRequest) -> dict:
    """Summarize recent metric trends or anomalies using Google Cloud Monitoring."""
    client_config = get_client_config()
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{client_config['project_id']}"

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=request.hours)

    query_request = {
        "name": project_name,
        "filter": f'metric.type="{request.metric_name}"',
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())},
        },
        "aggregation": {
            "alignment_period": {"seconds": 60},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        },
    }

    response = client.list_time_series(request=query_request)
    values = [point.value.double_value for series in response for point in series.points]

    if not values:
        return {"trend": "no data", "anomalies": []}

    anomalies = detect_anomalies(values, request.threshold) if request.threshold else []
    trend = "increasing" if values[-1] > values[0] else "decreasing" if values[-1] < values[0] else "stable"

    return {
        "trend": trend,
        "anomalies_count": sum(anomalies),
        "anomalies": anomalies,
        "values": values,
    }