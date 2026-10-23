from __future__ import annotations

from observability_client import cloudwatch_client
from observability_models import AggregateStats, MetricWindowRequest, normalize_cloudwatch_datapoints


CLOUDWATCH_NAMESPACE = "Amazon CloudWatch"


def aggregate_metric_stats(request: MetricWindowRequest) -> AggregateStats:
    client = cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        Dimensions=[{"Name": k, "Value": v} for k, v in request.dimensions.items()],
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=["Average", "Minimum", "Maximum", "Sum", "SampleCount"],
    )
    datapoints = normalize_cloudwatch_datapoints(response.get("Datapoints", []), "Average")
    if not datapoints:
        return AggregateStats(
            metric_name=request.metric_name,
            start_time=request.start_time,
            end_time=request.end_time,
            sample_count=0,
            minimum=None,
            maximum=None,
            average=None,
            sum=None,
            unit=None,
        )
    raw_points = sorted(response.get("Datapoints", []), key=lambda d: d["Timestamp"])
    sample_count = int(sum(point.get("SampleCount", 0) for point in raw_points))
    total_sum = sum(point.get("Sum", 0.0) for point in raw_points)
    weighted_avg = (total_sum / sample_count) if sample_count else None
    minimum = min((point.get("Minimum") for point in raw_points if point.get("Minimum") is not None), default=None)
    maximum = max((point.get("Maximum") for point in raw_points if point.get("Maximum") is not None), default=None)
    unit = raw_points[-1].get("Unit") if raw_points else None
    return AggregateStats(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        sample_count=sample_count,
        minimum=minimum,
        maximum=maximum,
        average=weighted_avg,
        sum=total_sum,
        unit=unit,
    )
