import datetime
from typing import Dict, List, Any
from google.cloud import monitoring_v3

class MetricSummary:
    def __init__(self, metric_name: str, summary_text: str, anomalies_detected: bool = False, raw_data: Any = None):
        self.metric_name = metric_name
        self.summary_text = summary_text
        self.anomalies_detected = anomalies_detected
        self.raw_data = raw_data

    def to_dict(self):
        return {
            "metric_name": self.metric_name,
            "summary_text": self.summary_text,
            "anomalies_detected": self.anomalies_detected,
            "raw_data": self.raw_data # Note: raw_data might be large
        }

def summarize_metric_trends(
    project_id: str,
    metric_type: str, # e.g., "compute.googleapis.com/instance/cpu/utilization"
    resource_type: str, # e.g., "gce_instance"
    end_time: datetime.datetime,
    duration_seconds: int = 3600, # how far back to look
    interval_seconds: int = 60, # aggregation interval
    filter_string: str = None, # additional MQL filter string
    project_location: str = "global"
) -> MetricSummary:
    
    client = monitoring_v3.MetricServiceClient()
    project_name = client.common_project_path(project_id)

    # Define the time interval
    start_time = end_time - datetime.timedelta(seconds=duration_seconds)
    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())}
    )

    # Define the aggregation
    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": interval_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    )

    query_filter = f'metric.type = "{metric_type}" AND resource.type = "{resource_type}"'
    if filter_string:
        query_filter += f' AND {filter_string}'

    response = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    summary_text = f"Metric '{metric_type}' trends:\n"
    anomalies_detected = False
    
    all_points = []
    for series in response.time_series:
        for point in series.points:
            value = point.value.double_value if point.value.HasField('double_value') else point.value.int64_value
            all_points.append(value)
            summary_text += f"  Timestamp: {point.interval.end_time.ToDatetime()}, Value: {value}\n"

    if all_points:
        avg_value = sum(all_points) / len(all_points)
        max_value = max(all_points)
        min_value = min(all_points)
        summary_text += f"Overall - Average: {avg_value:.2f}, Max: {max_value:.2f}, Min: {min_value:.2f}\n"

        # Simple anomaly detection: if max is much higher than average
        if max_value > avg_value * 1.5 and max_value - avg_value > 10: # arbitrary thresholds
            summary_text += "Potential anomaly: Maximum value significantly higher than average.\n"
            anomalies_detected = True

    return MetricSummary(metric_name=metric_type, summary_text=summary_text, anomalies_detected=anomalies_detected, raw_data=response)