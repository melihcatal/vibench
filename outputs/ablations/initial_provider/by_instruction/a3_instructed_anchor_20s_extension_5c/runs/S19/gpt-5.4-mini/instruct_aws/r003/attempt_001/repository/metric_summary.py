from datetime import datetime, timedelta, timezone

from observability_client import cloudwatch_client, load_observability_config


def metric_summary(metric_name: str, minutes: int = 60, namespace: str | None = None):
    cfg = load_observability_config()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    client = cloudwatch_client()
    response = client.get_metric_statistics(Namespace=namespace or cfg["cloudwatch_namespace"], MetricName=metric_name, StartTime=start_time, EndTime=end_time, Period=300, Statistics=["Average", "Maximum", "Minimum"])
    datapoints = response.get("Datapoints", [])
    avg = sum(float(d.get("Average", 0.0)) for d in datapoints) / len(datapoints) if datapoints else 0.0
    return {"metric_name": metric_name, "points": len(datapoints), "average": avg, "namespace": namespace or cfg["cloudwatch_namespace"]}
