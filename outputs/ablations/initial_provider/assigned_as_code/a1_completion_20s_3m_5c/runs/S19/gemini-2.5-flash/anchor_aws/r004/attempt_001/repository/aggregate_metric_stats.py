from datetime import datetime, timezone

from observability_client import get_cloudwatch_client
from observability_models import MetricQuery, MetricStatistic

def aggregate_metric_stats(payload, config=None):
    config = config or {}
    client = get_cloudwatch_client(region_name=config.get("region"))

    # Assuming payload directly maps to MetricQuery for simplicity for now
    # In a real scenario, you might normalize payload to MetricQuery object
    metric_query = MetricQuery(
        namespace=config["namespace"],
        metric_name=payload["metric"],
        dimensions=[{"Name": k, "Value": v} for k, v in config.get("dimensions", {}).items()],
        start_time=payload["start_time"],
        end_time=payload["end_time"],
        period_seconds=config.get("period_seconds", 60),
        statistics=payload.get("statistics", ["Average"])
    )

    response = client.get_metric_statistics(
        Namespace=metric_query.namespace,
        MetricName=metric_query.metric_name,
        Dimensions=metric_query.dimensions,
        StartTime=datetime.fromtimestamp(metric_query.start_time, timezone.utc),
        EndTime=datetime.fromtimestamp(metric_query.end_time, timezone.utc),
        Period=metric_query.period_seconds,
        Statistics=metric_query.statistics
    )

    stats = []
    for p in response["Datapoints"]:
        stat = MetricStatistic(timestamp=p["Timestamp"].timestamp())
        if "Average" in p: stat.average = float(p["Average"])
        if "Sum" in p: stat.sum = float(p["Sum"])
        if "Minimum" in p: stat.minimum = float(p["Minimum"])
        if "Maximum" in p: stat.maximum = float(p["Maximum"])
        if "SampleCount" in p: stat.sample_count = float(p["SampleCount"])
        stats.append(stat)
    
    return {"statistics": sorted(stats, key=lambda s: s.timestamp)}
