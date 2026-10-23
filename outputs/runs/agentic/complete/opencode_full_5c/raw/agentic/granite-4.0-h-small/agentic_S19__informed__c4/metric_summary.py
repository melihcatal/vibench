# metric_summary.py
# Summarize recent metric trends or anomalies

from observability_client import ObservabilityClient
from observability_models import MetricRequest, MetricResponse
import re
import os

ANOMALY_PATTERN = re.compile(r\"(?i)(anomaly|spike|drop)\")

def summarize_metric(service: str, metric: str, start: str, end: str,
                     window: str = None, dimensions: dict = None) -> str:
    """Return a human‑readable summary of the metric's recent behavior."""
    client = ObservabilityClient.get_client(service)
    # 1️⃣ Pull datapoints via the appropriate provider
    client_info = client["service"]
    if client_info == "datadog":
        import requests
        api = f"https://api.datadoghq.com/api/v1/query"
        headers = {"DD-API-KEY": client["api_key"], "DD-APPLICATION-KEY": client["app_key"]}
        payload = {
            "from": start,
            "to": end,
            "query": f"{metric}{{service:{service}}}",
            "interval": window or "1h"
        }
        resp = requests.get(api, headers=headers, params=payload)
        resp.raise_for_status()
        raw = resp.json()
        datapoints = [(pt["timestamp"], pt["value"]) for pt in raw["series"]]
    elif client_info == "google":
        from google.cloud import monitoring_v3
        client_obj = monitoring_v3.MetricServiceClient()
        project = client_obj.project_path(client_obj.project)
        series = client_obj.list_time_series(
            request={
                "name": project,
                "filter": f"metric.type = \"custom.googleapis.com/{metric}\"",
                "interval": {
                    "start_time": {"seconds": int(start)},
                    "end_time": {"seconds": int(end)}
                },
                "aggregation": {
                    "per_series_aligner": "ALIGN_MEAN",
                    "cross_series_reducer": "REDUCE_MEAN"
                }
            }
        )
        datapoints = [(p.interval.start_time.seconds, float(p.value.double_value)) for p in series]
    elif client_info == "aws":
        import boto3
        cw = boto3.client("cloudwatch", region_name="us-east-1")
        resp = cw.get_metric_statistics(
            Namespace="CustomMetrics",  # placeholder namespace
            MetricName=metric,
            StartTime=int(start),
            EndTime=int(end),
            Period=3600,
            Statistics=["Average"]
        )
        datapoints = [(pt["Timestamp"].timestamp(), pt["Average"]) for pt in resp["Datapoints"]]
    else:
        raise ValueError(f"Unsupported service {service} for summarization")

    # 2️⃣ Compute simple stats
    values = [v for _, v in datapoints]
    avg = sum(values) / len(values) if values else 0
    window_label = window or "<default>"
    # 3️⃣ Detect anomalies via keyword search in metric name / tags
    tags = [metric] + list(dimensions.values()) if dimensions else [metric]
    anomaly_present = any(ANOMALY_PATTERN.search(tag) for tag in tags)
    # 4️⃣ Build a concise report
    lines = [
        f"Metric: {metric} (Window: {window_label})",
        f"Observations (count: {len(datapoints)}): Avg = {avg:.2f}",
        "Trend:" + (" anomalous" if anomaly_present else " normal")
    ]
    return "\n".join(lines)
