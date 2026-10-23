import os

from google.cloud import monitoring_v3


def load_observability_config(config=None):
    config = config or {}
    merged = {
        "project_id": config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT"),
        "period_seconds": int(config.get("period_seconds", os.environ.get("METRICS_PERIOD_SECONDS", 60))),
    }
    if not merged["project_id"]:
        raise ValueError("project_id is required")
    return merged


def get_monitoring_client():
    return monitoring_v3.MetricServiceClient()


def metric_project_name(project_id):
    return f"projects/{project_id}"
