import json

from google.cloud import monitoring_v3

from observability_client import MonitoringClient
from observability_models import MetricAggregate

def aggregate_metric_stats(payload, config=None):
    config = config or {}
    client = MonitoringClient(project_id=config['project_id'])

    metric_filter = "metric.type = " + json.dumps(payload["metric"])
    start_time = payload["start_time"]
    end_time = payload["end_time"]
    period_seconds = config.get("period_seconds", 60)

    aggregations = {
        "mean": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        "min": monitoring_v3.Aggregation.Aligner.ALIGN_MIN,
        "max": monitoring_v3.Aggregation.Aligner.ALIGN_MAX,
        "sum": monitoring_v3.Aggregation.Aligner.ALIGN_SUM,
        "count": monitoring_v3.Aggregation.Aligner.ALIGN_COUNT,
    }

    results = {}
    for agg_name, aligner in aggregations.items():
        series = client.list_time_series(
            metric_filter=metric_filter,
            start_time=start_time,
            end_time=end_time,
            aligner=aligner,
            period_seconds=period_seconds,
        )
        for ts in series:
            for point in ts.points:
                timestamp = point.interval.end_time.timestamp()
                kind = point.value._pb.WhichOneof("value")
                if kind not in ("double_value", "int64_value"):
                    raise ValueError("Expected a scalar numeric metric")
                value = float(getattr(point.value, kind))
                if timestamp not in results:
                    results[timestamp] = {"timestamp": timestamp}
                results[timestamp][agg_name] = value
    
    # Convert results to a list of MetricAggregate objects
    # Fill missing values with None or a sensible default if any aggregation type didn't return data for a timestamp
    aggregated_data = [
        MetricAggregate(
            timestamp=ts_data["timestamp"],
            mean=ts_data.get("mean"),
            min=ts_data.get("min"),
            max=ts_data.get("max"),
            sum=ts_data.get("sum"),
            count=ts_data.get("count"),
        )
        for ts_data in results.values()
    ]
    
    return {"aggregates": sorted(aggregated_data, key=lambda a: a.timestamp)}
