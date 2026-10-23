from google.cloud import monitoring_v3
import os
import datetime

def aggregate_metric_stats(project_id: str, metric_type: str, end_time_str: str, duration_minutes: int, aggregator: str = "mean"):
    """Retrieves aggregated statistics for a metric over a time window using Google Cloud Monitoring."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%SZ")
    start_time = end_time - datetime.timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time=end_time.isoformat("T") + "Z",
        start_time=start_time.isoformat("T") + "Z",
    )

    # Example filter: "metric.type = \"logging.googleapis.com/log_entry_count\""
    filter_str = f'metric.type = "{metric_type}"'

    # Map common aggregators to Monitoring API Aligner values
    # https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/list#aligner
    aggregation_aligner_map = {
        "mean": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        "min": monitoring_v3.Aggregation.Aligner.ALIGN_MIN,
        "max": monitoring_v3.Aggregation.Aligner.ALIGN_MAX,
        "sum": monitoring_v3.Aggregation.Aligner.ALIGN_SUM,
        "count": monitoring_v3.Aggregation.Aligner.ALIGN_COUNT,
    }
    selected_aligner = aggregation_aligner_map.get(aggregator.lower(), monitoring_v3.Aggregation.Aligner.ALIGN_MEAN)

    # Define aggregation
    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 60 * 5}, # 5-minute alignment period
        per_series_aligner=selected_aligner,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_NONE, # No cross-series reduction for this task
        group_by_fields=["resource.type", "resource.labels.instance_id"], # Example grouping
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
    for series in results:
        for point in series.points:
            aggregated_data.append({
                "value": point.value.double_value or point.value.int64_value or point.value.string_value or str(point.value.bool_value),
                "timestamp": point.interval.end_time.isoformat(),
                "metric_labels": dict(series.metric.labels),
                "resource_labels": dict(series.resource.labels),
            })
    return aggregated_data

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    metric_to_aggregate = "compute.googleapis.com/instance/cpu/usage_time" # Example metric
    end_time_example = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    duration_example = 120 # minutes
    aggregator_type = "mean"

    print(f"Aggregating metric '{metric_to_aggregate}' for project '{project_id}' with '{aggregator_type}'...")
    data = aggregate_metric_stats(project_id, metric_to_aggregate, end_time_example, duration_example, aggregator_type)
    print(f"Retrieved {len(data)} aggregated data points.")
    # print(data) # Uncomment to see actual data
