import os
from functools import lru_cache
from google.cloud import monitoring_v3


def project_id():
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT") or os.getenv("GCLOUD_PROJECT")


@lru_cache(maxsize=1)
def monitoring_client():
    return monitoring_v3.MetricServiceClient()


def metric_type(name):
    if name.startswith("custom.googleapis.com/") or name.startswith("logging.googleapis.com/"):
        return name
    return f"custom.googleapis.com/{name}"


def project_name():
    pid = project_id()
    return f"projects/{pid}" if pid else None
