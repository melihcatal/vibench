from datetime import datetime, timezone

from observability_client import get_cloudwatch_client
from observability_models import MetricQuery, MetricDatapoint, MetricStatistics


def compare_metric_series(payload, config=None):
    config = config or {}
    client = get_cloudwatch_client(config.get("region"))

    results = {}

    # Query for series A
    dimensions_a = {**config.get("dimensions", {}), **payload.get("dimensions_a", {})}
    metric_query_a = MetricQuery(
        namespace=config["namespace"],
        metric_name=payload["metric"],
        start_time=payload["start_time"],
        end_time=payload["end_time"],
        period_seconds=config.get("period_seconds", 60),
        statistics=payload.get("statistics", ["Average"]),
        dimensions=dimensions_a
    )

    response_a = client.get_metric_statistics(
        Namespace=metric_query_a.namespace,
        MetricName=metric_query_a.metric_name,
        Dimensions=[{"Name": k, "Value": v} for k, v in metric_query_a.dimensions.items()],
        StartTime=datetime.fromtimestamp(metric_query_a.start_time, timezone.utc),
        EndTime=datetime.fromtimestamp(metric_query_a.end_time, timezone.utc),
        Period=metric_query_a.period_seconds,
        Statistics=metric_query_a.statistics
    )

    points_a = []
    for p in response_a["Datapoints"]:
        for stat in metric_query_a.statistics:
            if stat in p:
                points_a.append(MetricDatapoint(timestamp=p["Timestamp"].timestamp(), value=float(p[stat])))
    results["series_a"] = MetricStatistics(datapoints=sorted(points_a, key=lambda p: p.timestamp), label="Series A")

    # Query for series B
    dimensions_b = {**config.get("dimensions", {}), **payload.get("dimensions_b", {})}
    metric_query_b = MetricQuery(
        namespace=config["namespace"],
        metric_name=payload["metric"],
        start_time=payload["start_time"],
        end_time=payload["end_time"],
        period_seconds=config.get("period_seconds", 60),
        statistics=payload.get("statistics", ["Average"]),
        dimensions=dimensions_b
    )

    response_b = client.get_metric_statistics(
        Namespace=metric_query_b.namespace,
        MetricName=metric_query_b.metric_name,
        Dimensions=[{"Name": k, "Value": v} for k, v in metric_query_b.dimensions.items()],
        StartTime=datetime.fromtimestamp(metric_query_b.start_time, timezone.utc),
        EndTime=datetime.fromtimestamp(metric_query_b.end_time, timezone.utc),
        Period=metric_query_b.period_seconds,
        Statistics=metric_query_b.statistics
    )

    points_b = []
    for p in response_b["Datapoints"]:
        for stat in metric_query_b.statistics:
            if stat in p:
                points_b.append(MetricDatapoint(timestamp=p["Timestamp"].timestamp(), value=float(p[stat])))
    results["series_b"] = MetricStatistics(datapoints=sorted(points_b, key=lambda p: p.timestamp), label="Series B")

    return results
