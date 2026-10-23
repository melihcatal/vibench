from datetime import datetime, timedelta, timezone

from observability_client import cloudwatch_client, load_config


def metric_summary(metric_name=None, namespace=None, minutes=60):
    cfg = load_config(namespace=namespace, metric_name=metric_name)
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    client = cloudwatch_client()
    return client.get_metric_statistics(Namespace=cfg.namespace, MetricName=cfg.metric_name, StartTime=start_time, EndTime=end_time, Period=300, Statistics=["Average", "Maximum"])
