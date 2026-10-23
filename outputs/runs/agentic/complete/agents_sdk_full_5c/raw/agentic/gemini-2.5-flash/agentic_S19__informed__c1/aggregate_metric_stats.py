
import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3

def aggregate_metric_stats(project_id: str, metric_type: str, minutes: int = 60, reducer_type: str = "REDUCE_MEAN"):
    """
    Retrieves aggregated statistics for a metric over a time window using Google Cloud Monitoring.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    start_time = (now - timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(now.timestamp())},
        start_time={"seconds": int((now - timedelta(minutes=minutes)).timestamp())},
    )

    # Example filter for a generic metric
    filter_str = f'metric.type = "{metric_type}"'

    # Aggregation parameters
    # https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/list#aggregation
    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 60 * 5},  # Align to 5-minute intervals
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN, # Or ALIGN_DELTA, ALIGN_RATE, etc.
        cross_series_reducer=getattr(monitoring_v3.Aggregation.Reducer, reducer_type, monitoring_v3.Aggregation.Reducer.REDUCE_MEAN),
        group_by_fields=["resource.type", "resource.label.instance_name"], # Group by resource type and instance name
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    aggregated_data = []
    for ts in results:
        for point in ts.points:
            aggregated_data.append({
                "timestamp": point.interval.end_time,
                "value": point.value.double_value or point.value.int64_value,
                "metric_labels": {k: v for k, v in ts.metric.labels.items()},
                "resource_labels": {k: v for k, v in ts.resource.labels.items()},
            })
    return aggregated_data

if __name__ == "__main__":
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    data = aggregate_metric_stats(project_id, metric_type, minutes=60, reducer_type="REDUCE_MAX")
    print(f"Retrieved {len(data)} aggregated data points for {metric_type}:")
    for d in data[:5]:
        print(d)
