import os
from observable_client import get_provider_client, normalize_response
from observable_models import AggregateMetricStatsRequest, AggregateMetricStatsResponse

PROVIDER = os.getenv("METRICS_PROVIDER", "datadog")


def aggregate_metric_stats(
    request: AggregateMetricStatsRequest,
) -> AggregateMetricStatsResponse:
    """Retrieve aggregated statistics (e.g., sum, avg, max) for a metric over a window.

    Args:
        request: Metric name and window definition (and optional resolution).

    Returns:
        Normalized dict containing aggregated values.
    """
    client = get_provider_client(PROVIDER)
    if PROVIDER == "datadog":
        response = client.metrics.query(
            metric=request.metric_name,
            start=request.start_time,
            end=request.end_time,
            query=f"avg:{request.metric_name} over {request.window} as_rate",
        )
    elif PROVIDER == "ibm_monitoring":
        response = client.aggregate_metric(
            metric=request.metric_name,
            window=request.window,
        )
    elif PROVIDER == "azure":
        response = client.metrics_list(
            resource="",
            metric=request.metric_name,
            timespan=f"{request.start_time},{request.end_time}",
            interval="PT1M",
            aggregation="average",
        )
    elif PROVIDER == "cloudwatch":
        response = client.get_metric_statistics(
            Namespace="AWS/YourNamespace",
            MetricName=request.metric_name,
            StartTime=request.start_time,
            EndTime=request.end_time,
            Period=300,
            Statistics=["Sum", "Average", "Maximum"],
        )
    elif PROVIDER == "alibaba":
        response = client.DescribeMetricStatistic(
            metricName=request.metric_name,
            startTime=request.start_time,
            endTime=request.end_time,
            window=request.window,
        )
    elif PROVIDER == "google":
        # Google Monitoring allows aggregations via aggregationSettings
        client = get_provider_client(PROVIDER)
        name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/metricDescriptors/{request.metric_name}"
        response = client.list_time_series(
            name=name,
            filter=f"metric.type='{request.metric_name}'",
            interval={"startTime": request.start_time, "endTime": request.end_time},
            aggregation={
                "alignmentPeriod": request.window,
                "perSeriesAligner": "ALIGN_MEAN",
                "crossSeriesReducer": "REDUCE_SUM",
            },
            view="FULL",
        )
    else:
        raise ValueError(f"Unsupported provider for aggregation: {PROVIDER}")

    normalized = normalize_response(response, PROVIDER)
    return AggregateMetricStatsResponse(**normalized)


if __name__ == "__main__":
    # Sample usage
    req = AggregateMetricStatsRequest(
        metric_name="system.cpu.user",
        window="1h",
    )
    stats = aggregate_metric_stats(req)
    print("Aggregated stats:", stats.aggregates)
