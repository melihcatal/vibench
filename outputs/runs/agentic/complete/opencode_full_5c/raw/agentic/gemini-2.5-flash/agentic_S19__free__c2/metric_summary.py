from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricQuery, MetricQueryResponse


def summarize_metric_trends(query: MetricQuery) -> str:
    client = get_monitoring_client()
    project_name = f"projects/{query.project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(query.interval_end_time)},
        start_time={"seconds": int(query.interval_start_time)},
    )

    metric_filter = f'metric.type = "{query.metric_type}"'
    if query.filter:
        metric_filter += f" AND {query.filter}"

    # Aggregate for a simple trend summary (e.g., average over the period)
    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": query.aggregation_period_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=query.group_by_fields
        if query.group_by_fields
        else ["resource.instance_id"],
    )

    result = client.list_time_series(
        name=project_name,
        filter=metric_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    summary_lines = []
    if not result:
        return "No data found for the given metric and time window."

    for ts in result:
        values = [
            point.value.double_value
            if point.value.double_value
            else point.value.int64_value
            for point in ts.points
            if (
                point.value.double_value is not None
                or point.value.int64_value is not None
            )
        ]
        if values:
            avg_value = sum(values) / len(values)
            max_value = max(values)
            min_value = min(values)
            summary_lines.append(
                f"  Resource {ts.resource.labels.get('instance_id', 'N/A')} (Metric: {ts.metric.labels.get('metric_name', query.metric_type)}): Avg={avg_value:.2f}, Max={max_value:.2f}, Min={min_value:.2f}"
            )
        else:
            summary_lines.append(
                f"  Resource {ts.resource.labels.get('instance_id', 'N/A')} (Metric: {ts.metric.labels.get('metric_name', query.metric_type)}): No numerical data points."
            )

    return "Metric Trend Summary:\n" + "\n".join(summary_lines)


from typing import Dict

if __name__ == "__main__":
    project_id = get_project_id()
    end_time = 1678886400  # Example timestamp (March 15, 2023 12:00:00 PM UTC)
    start_time = end_time - 3600  # 1 hour before

    # Example usage: summarize CPU utilization for all GCE instances
    metric_query = MetricQuery(
        project_id=project_id,
        metric_type="compute.googleapis.com/instance/cpu/utilization",
        interval_end_time=str(end_time),
        interval_start_time=str(start_time),
        aggregation_period_seconds=300,
        group_by_fields=["resource.instance_id"],
    )

    summary = summarize_metric_trends(metric_query)
    print(summary)
