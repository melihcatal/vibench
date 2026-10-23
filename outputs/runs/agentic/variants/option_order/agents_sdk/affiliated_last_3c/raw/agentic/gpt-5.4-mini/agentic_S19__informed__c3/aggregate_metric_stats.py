from __future__ import annotations

from observability_client import cloudwatch_client, default_namespace
from observability_models import MetricStatsResponse, MetricWindowRequest, dimensions_to_list


def aggregate_metric_stats(request: MetricWindowRequest) -> MetricStatsResponse:
    client = cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=request.namespace or default_namespace(),
        MetricName=request.metric_name,
        Dimensions=dimensions_to_list(request.dimensions),
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=["Minimum", "Maximum", "Average", "Sum", "SampleCount"],
    )
    stats = response.get("Datapoints", [])
    if not stats:
        return MetricStatsResponse(request.metric_name, request.namespace, None, None, None, None, None)
    latest = max(stats, key=lambda item: item["Timestamp"])
    return MetricStatsResponse(
        metric_name=request.metric_name,
        namespace=request.namespace,
        minimum=float(latest.get("Minimum")) if latest.get("Minimum") is not None else None,
        maximum=float(latest.get("Maximum")) if latest.get("Maximum") is not None else None,
        average=float(latest.get("Average")) if latest.get("Average") is not None else None,
        sum=float(latest.get("Sum")) if latest.get("Sum") is not None else None,
        sample_count=float(latest.get("SampleCount")) if latest.get("SampleCount") is not None else None,
    )
