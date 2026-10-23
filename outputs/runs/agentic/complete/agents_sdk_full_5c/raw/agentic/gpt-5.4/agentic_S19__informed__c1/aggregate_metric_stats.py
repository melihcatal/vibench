from __future__ import annotations

from observability_client import DEFAULT_CLOUDWATCH_NAMESPACE, get_cloudwatch_client
from observability_models import AggregateStatsResponse, MetricWindowRequest, normalize_cloudwatch_datapoints, summarize_points



def aggregate_metric_stats(request: MetricWindowRequest) -> AggregateStatsResponse:
    client = get_cloudwatch_client(region_name=request.region_name)
    response = client.get_metric_statistics(
        namespace=request.namespace or DEFAULT_CLOUDWATCH_NAMESPACE,
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        period=request.period,
        statistics=["Average", "Minimum", "Maximum", "Sum", "SampleCount"],
        dimensions=request.dimensions,
    )
    datapoints = normalize_cloudwatch_datapoints(response.get("Datapoints", []), "Average")
    summary = summarize_points(datapoints)
    return AggregateStatsResponse(
        metric_name=request.metric_name,
        namespace=request.namespace,
        statistics={
            "minimum": summary["min"],
            "maximum": summary["max"],
            "average": summary["avg"],
            "latest": summary["latest"],
            "sum": sum(point.value for point in datapoints) if datapoints else None,
        },
        sample_count=len(datapoints),
        unit=datapoints[-1].unit if datapoints else None,
    )
