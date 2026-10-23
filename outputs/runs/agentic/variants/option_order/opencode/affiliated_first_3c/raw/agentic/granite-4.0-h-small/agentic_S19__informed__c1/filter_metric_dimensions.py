import os
from observable_client import get_provider_client, normalize_response
from observable_models import FilterMetricDimensionsRequest, FilterMetricDimensionsResponse

PROVIDER = os.getenv("METRICS_PROVIDER", "datadog")


def filter_metric_dimensions(request: FilterMetricDimensionsRequest) -> FilterMetricDimensionsResponse:
    """Query metric data filtered by label dimensions (resource labels or tags)."""
    client = get_provider_client(PROVIDER)
    if PROVIDER == "datadog":
        # Datadog tags: key:value syntax in the query
        tag_filter = " AND ".join([f"{k}:{v}" for k, vs in request.dimensions.items() for v in vs])
        response = client.metrics.query(
            metric=request.metric_name,
            start=request.start_time,
            end=request.end_time,
            query=f"avg:{request.metric_name}{{{tag_filter}}}",
        )
    elif PROVIDER == "ibm_monitoring":
        # IBM uses label filters directly
        response = client.query_metric(
            metric=request.metric_name,
            start=request.start_time,
            end=request.end_time,
            filters=request.dimensions,
        )
    elif PROVIDER == "azure":
        # Azure supports dimension filters via dimensionFilters list
        response = client.metrics_list(
            resource="",
            metric=request.metric_name,
            timespan=f"{request.start_time},{request.end_time}",
            interval="PT1M",
            aggregation="average",
            dimension_filters=[{"name": k, "values": vs} for k, vs in request.dimensions.items()],
        )
    elif PROVIDER == "cloudwatch":
        # CloudWatch does not support label filtering via SDK; use metric math instead
        raise NotImplementedError("CloudWatch label filtering not implemented")
    elif PROVIDER == "alibaba":
        # Alibaba allows label filtering via tags/labels
        response = client.DescribeMetricLast(
            metricName=request.metric_name,
            startTime=request.start_time,
            endTime=request.end_time,
            labels=request.dimensions,
        )
    elif PROVIDER == "google":
        # Google supports filtering via metric.type and resource.labels
        client = get_provider_client(PROVIDER)
        name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/metricDescriptors/{request.metric_name}"
        response = client.list_time_series(
            name=name,
            filter=f"
                metric.type='{request.metric_name}' AND resource.labels.environment='{list(request.dimensions.values())[0][0]}'",
            interval={"startTime": request.start_time, "endTime": request.end_time},
            view="FULL",
        )
    else:
        raise ValueError(f"Unsupported provider for label filtering: {PROVIDER}")

    normalized = normalize_response(response, PROVIDER)
    return FilterMetricDimensionsResponse(**normalized)

if __name__ == "__main__":
    # Example: filter CPU user metric by environment label
    req = FilterMetricDimensionsRequest(
        metric_name="system.cpu.user",
        dimensions={"environment": ["prod", "staging"]},
        start_time="2024-07-01T12:00:00Z",
        end_time="2024-07-01T13:00:00Z",
    )
    resp = filter_metric_dimensions(req)
    print("Filtered datapoints count:", len(resp.filtered_datapoints))
