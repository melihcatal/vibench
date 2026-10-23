from datetime import datetime, timezone

from observability_client import get_cloudwatch_client
from observability_models import MetricQuery, MetricDatapoint, MetricStatistics


def aggregate_metric_stats(payload, config=None):
    config = config or {}
    client = get_cloudwatch_client(config.get("region"))

    metric_query = MetricQuery(
        namespace=config["namespace"],
        metric_name=payload["metric"],
        start_time=payload["start_time"],
        end_time=payload["end_time"],
        period_seconds=config.get("period_seconds", 60),
        statistics=payload.get("statistics", ["Average"]),
        dimensions=config.get("dimensions", {})
    )

    response = client.get_metric_statistics(
        Namespace=metric_query.namespace,
        MetricName=metric_query.metric_name,
        Dimensions=[{"Name": k, "Value": v} for k, v in metric_query.dimensions.items()],
        StartTime=datetime.fromtimestamp(metric_query.start_time, timezone.utc),
        EndTime=datetime.fromtimestamp(metric_query.end_time, timezone.utc),
        Period=metric_query.period_seconds,
        Statistics=metric_query.statistics
    )

    points = []
    for p in response["Datapoints"]:
        for stat in metric_query.statistics:
            if stat in p:
                points.append(MetricDatapoint(timestamp=p["Timestamp"].timestamp(), value=float(p[stat])))

    return MetricStatistics(datapoints=sorted(points, key=lambda p: p.timestamp), label=metric_query.metric_name)
