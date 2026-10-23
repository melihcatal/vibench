from google.cloud import monitoring_v3
from datetime import datetime, timedelta
from typing import Dict, List, Any

def summarize_metric_trends(project_id: str, metric_type: str, minutes_ago: int = 60, interval_seconds: int = 60) -> Dict[str, Any]:
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(now.timestamp())},
        start_time={'seconds': int(start_time.timestamp())},
    )

    query_filter = f'metric.type = "{metric_type}"'

    response = client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    summary_data = []
    for series in response.time_series:
        metric_data = {
            "metric_kind": monitoring_v3.MetricDescriptor.MetricKind(series.metric_kind).name,
            "value_type": monitoring_v3.MetricDescriptor.ValueType(series.value_type).name,
            "resource_labels": {k: v for k, v in series.resource.labels.items()},
            "metric_labels": {k: v for k, v in series.metric.labels.items()},
            "points": []
        }
        for point in series.points:
            value = None
            if point.value.HasField("int64_value"):
                value = point.value.int64_value
            elif point.value.HasField("double_value"):
                value = point.value.double_value
            elif point.value.HasField("bool_value"):
                value = point.value.bool_value
            elif point.value.HasField("string_value"):
                value = point.value.string_value

            metric_data["points"].append({
                "timestamp": point.interval.end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "value": value
            })
        summary_data.append(metric_data)

    # Basic anomaly detection (e.g., simple thresholding or rate of change)
    anomalies = []
    for metric_entry in summary_data:
        points = metric_entry["points"]
        if len(points) > 1:
            # Simple trend: check if the last value is significantly different from the average
            values = [p["value"] for p in points if isinstance(p["value"], (int, float))]
            if values:
                avg_value = sum(values) / len(values)
                last_value = values[-1]
                if avg_value != 0 and abs((last_value - avg_value) / avg_value) > 0.2: # 20% deviation
                    anomalies.append(f"Potential anomaly in {metric_type} for resource {metric_entry['resource_labels']}. Last value: {last_value}, Average: {avg_value:.2f}")

    return {
        "summary_data": summary_data,
        "anomalies": anomalies
    }
