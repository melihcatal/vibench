from __future__ import annotations

from observability_client import CloudWatchMetricsClient
from observability_models import MetricStatistics, MetricWindowRequest


def aggregate_metric_stats(request: MetricWindowRequest) -> MetricStatistics:
    client = CloudWatchMetricsClient()
    response = client.list_metric_data(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        dimensions=request.dimensions,
        period=request.period,
        stat=request.statistic,
    )
    datapoints = response.get("Datapoints", [])
    if not datapoints:
        return MetricStatistics(metric_name=request.metric_name, start_time=request.start_time, end_time=request.end_time)

    values = [float(item.get(request.statistic, item.get("Average", 0.0))) for item in datapoints if item.get(request.statistic, item.get("Average")) is not None]
    return MetricStatistics(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        minimum=min(values),
        maximum=max(values),
        average=sum(values) / len(values),
        sum=sum(values),
        sample_count=float(len(values)),
        unit=datapoints[0].get("Unit"),
    )
