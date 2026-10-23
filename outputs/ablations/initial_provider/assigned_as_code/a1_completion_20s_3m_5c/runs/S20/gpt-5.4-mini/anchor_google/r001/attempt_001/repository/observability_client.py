import os
from dataclasses import dataclass

from google.cloud import logging_v2


@dataclass
class ObservabilityConfig:
    project_id: str
    log_name: str
    service_name: str
    location: str


def load_config(config=None):
    config = config or {}
    return ObservabilityConfig(
        project_id=config.get("project_id") or os.environ["GOOGLE_CLOUD_PROJECT"],
        log_name=config.get("log_name") or os.environ.get("GOOGLE_CLOUD_LOG_NAME", "application"),
        service_name=config.get("service_name") or os.environ.get("GOOGLE_CLOUD_SERVICE_NAME", "app"),
        location=config.get("location") or os.environ.get("GOOGLE_CLOUD_LOCATION", "global"),
    )


def make_client(config=None):
    cfg = load_config(config)
    client = logging_v2.Client(project=cfg.project_id)
    return cfg, client
