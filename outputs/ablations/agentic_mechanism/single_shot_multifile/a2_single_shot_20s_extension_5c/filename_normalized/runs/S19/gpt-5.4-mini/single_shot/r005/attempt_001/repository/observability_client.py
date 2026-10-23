import os
from dataclasses import dataclass
from typing import Optional
import requests

PROMETHEUS_API_BASE = os.getenv("PROMETHEUS_API_BASE", "https://monitoring.googleapis.com/v3")
PROMETHEUS_BEARER_TOKEN = os.getenv("PROMETHEUS_BEARER_TOKEN", "")
PROMETHEUS_PROJECT = os.getenv("PROMETHEUS_PROJECT", "")

@dataclass
class ObservabilityConfig:
    api_base: str = PROMETHEUS_API_BASE
    bearer_token: str = PROMETHEUS_BEARER_TOKEN
    project: str = PROMETHEUS_PROJECT


def get_config() -> ObservabilityConfig:
    return ObservabilityConfig()


def build_session(config: Optional[ObservabilityConfig] = None) -> requests.Session:
    cfg = config or get_config()
    session = requests.Session()
    if cfg.bearer_token:
        session.headers.update({"Authorization": f"Bearer {cfg.bearer_token}"})
    session.headers.update({"Content-Type": "application/json"})
    return session


def metric_path(metric_type: str, project: Optional[str] = None) -> str:
    cfg = get_config()
    prj = project or cfg.project
    if not prj:
        raise ValueError("PROMETHEUS_PROJECT is required")
    return f"projects/{prj}/timeSeries"
