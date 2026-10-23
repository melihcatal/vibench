import os
from observable_client import get_provider_client
from observable_models import CompareMetricSeriesRequest, CompareMetricSeriesResponse

PROVIDER = os.getenv("METRICS_PROVIDER", "datadog")


def compare_metric_series(request: CompareMetricSeriesRequest) -> CompareMetricSeriesResponse:
    """Compare metric values across multiple resources or dimension filters for the same window.

    Args:
        request: List of resource identifiers (or tag filters) and the metric name and window.

    Returns:
        Structured comparison result that highlights differences or trends.
    """
    client = get_provider_client(PROVIDER)
    if PROVIDER == "datadog":
        # Datadog supports a single query for multiple series; we build a JSON query
        series_queries = [f"{q}:avg:{request.metric_name}" for q in request.resources]
        query = "{ "series": [{"q": q} for q in series_queries] }"
        response = client.metrics.query(query=json.loads(query))  # placeholder; real API would handle list
    elif PROVIDER == "ibm_monitoring":
        # IBM can fetch multiple series by passing a list of metric names (or resource IDs)
        responses = []
        for r in request.resources:
            resp = client.query_metric(
                metric=request.metric_name,
                start=request.start_time,
                end=request.end_time,
                resource=r,
            )
            responses.append(resp)
        # Simple merge of series
        data = [s.get('datapoints', []) for s in responses]
    elif PROVIDER == "azure":
        # Azure needs separate calls per resource; collect each series
        series = {}
        for r in request.resources:
            resp = client.metrics_list(
                resource=r,
                metric=request.metric_name,
                timespan=f"{request.start_time},{request.end_time}",
                interval="PT1M",
                aggregation="average",
            )
            series[r] = resp.get('value', [])
        data = list(series.values())
    elif PROVIDER in ("cloudwatch", "alibaba", "google"):
        # For providers that do not natively support multi‑series comparison, we fetch each series individually
        series = {}
        for r in request.resources:
            resp = client.get_metric_statistics(
                Namespace="AWS/YourNamespace",
                MetricName=request.metric_name,
                StartTime=request.start_time,
                EndTime=request.end_time,
                Period=60,
                Statistics=["Average"],
                Dimensions=[{"Name": "Resource", "Value": r}],
            )
            series[r] = resp.get('Datapoints', [])
        data = list(series.values())
    else:
        raise ValueError(f"Unsupported provider for cross‑series comparison: {PROVIDER}")

    # Simple comparison payload: list each series with its first datapoint for illustration
    comparison = [{"resource": r, "first_value": d[0]["value"] if d else None} for r, d in series.items()]
    return CompareMetricSeriesResponse(series_comparison=comparison)

if __name__ == "__main__":
    # Example: compare CPU usage across two VM instances
    req = CompareMetricSeriesRequest(
        resources=["vm-01", "vm-02"],
        metric_name="system.cpu.user",
        start_time="2024-07-01T12:00:00Z",
        end_time="2024-07-01T13:00:00Z",
    )
    result = compare_metric_series(req)
    print("Comparison result:", result.series_comparison)
