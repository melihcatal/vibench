import os

from google.cloud import monitoring_v3


def load_observability_config(config=None):
    merged = dict(config or {})
    if "project_id" not in merged:
        merged["project_id"] = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    if "period_seconds" not in merged:
        merged["period_seconds"] = int(os.environ.get("METRICS_PERIOD_SECONDS", "60"))
    return merged


def monitoring_client():
    return monitoring_v3.MetricServiceClient()


def project_name(project_id):
    return f"projects/{project_id}"
