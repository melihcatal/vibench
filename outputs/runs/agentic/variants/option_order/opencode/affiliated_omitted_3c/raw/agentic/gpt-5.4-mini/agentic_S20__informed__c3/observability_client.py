import os
from dataclasses import dataclass

from google.cloud import logging as cloud_logging


@dataclass(frozen=True)
class ObservabilityConfig:
    project_id: str
    log_name: str


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        project_id=os.environ.get(
            "GOOGLE_CLOUD_PROJECT", os.environ.get("GCLOUD_PROJECT", "")
        ),
        log_name=os.environ.get("OBSERVABILITY_LOG_NAME", "application"),
    )


def build_client() -> cloud_logging.Client:
    return cloud_logging.Client(project=load_config().project_id or None)


def get_logger():
    cfg = load_config()
    return build_client().logger(cfg.log_name)
