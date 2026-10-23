import os

from google.cloud import monitoring_v3, storage


def load_config(config=None):
    merged = dict(config or {})
    if "project_id" not in merged:
        merged["project_id"] = os.environ["GOOGLE_CLOUD_PROJECT"]
    merged.setdefault("period_seconds", int(os.environ.get("METRICS_PERIOD_SECONDS", "60")))
    merged.setdefault("location", os.environ.get("METRICS_LOCATION", "global"))
    return merged


def monitoring_client():
    return monitoring_v3.MetricServiceClient()


def storage_client():
    return storage.Client()
