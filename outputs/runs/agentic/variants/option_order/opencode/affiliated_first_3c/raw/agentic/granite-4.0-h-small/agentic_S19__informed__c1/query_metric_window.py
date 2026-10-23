import os
from observable_client import get_provider_client, normalize_response
from observable_models import QueryMetricWindowRequest, QueryMetricWindowResponse

PROVIDER = os.getenv("METRICS_PROVIDER", "datadog")  # default provider


def query_metric_window(request: QueryMetricWindowRequest) -> QueryMetricWindowResponse:
    """Retrieve raw datapoints for a metric over a time window using the configured provider.

    Args:
        request: Query parameters (metric name, start/end timestamps, limit).

    Returns:
        Normalized response with datapoints and optional meta information.
    """
    client = get_provider_client(PROVIDER)
    if PROVIDER == "datadog":
        # Datadog API v2: metric query endpoint
        response = client.metrics.query(
            metric=request.metric_name,
            start=request.start_time,
            end=request.end_time,
            query=f"avg:{request.metric_name}{request.limit:+}",  # placeholder query string
        )
    elif PROVIDER == "ibm_monitoring":
        response = client.query_metric(
            metric=request.metric_name,
            start=request.start_time,
            end=request.end_time,
            limit=request.limit,
        )
    elif PROVIDER == "azure":
        # Azure Monitor Metrics query with timeGrain, interval and aggregation
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
            Period=60,
            Statistics=["Average"],
        )
    elif PROVIDER == "alibaba":
        response = client.DescribeMetricLast(
            namespace=",
            metricName=request.metric_name,
            startTime=request.start_time,
            endTime=request.end_time,
            limit=request.limit,
        )
    elif PROVIDER == "google":
        # Google Monitoring API time series query
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        client = get_provider_client(PROVIDER)
        response = client.list_time_series(
            name=f"projects/{project_id}",
            filter=f"metric.type=\"custom.googleapis.com/{request.metric_name}\"",
            interval={"startTime": request.start_time, "endTime": request.end_time},
            view="HEADERS",
        )
    else:
        raise ValueError(f"Unsupported provider for query: {PROVIDER}")

    # Normalize raw response to a common format
    normalized = normalize_response(response, PROVIDER)
    return QueryMetricWindowResponse(**normalized)

if __name__ == "__main__":
    # Example usage (run with env vars set for the chosen provider)
    from datetime import datetime, timedelta

    start = (datetime.utcnow() - timedelta(hours=2)).isoformat() + "Z"
    end = datetime.utcnow().isoformat() + "Z"
    req = QueryMetricWindowRequest(
        metric_name="system.cpu.user",
        start_time=start,
        end_time=end,
        limit=200,
    )
    resp = query_metric_window(req)
    print("QueryMetricWindowResponse:", resp.datapoints[:5])
