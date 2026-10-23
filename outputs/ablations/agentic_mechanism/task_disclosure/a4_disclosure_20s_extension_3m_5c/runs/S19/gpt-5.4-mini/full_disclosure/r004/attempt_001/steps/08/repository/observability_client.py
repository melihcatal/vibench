from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass(frozen=True)
class ManagedMetricsConfig:
    api_key: str
    project_id: Optional[str]
    base_url: str = "https://eu.mixpanel.com"
    timeout_seconds: int = 30


def load_managed_metrics_config(
    *,
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout_seconds: Optional[int] = None,
) -> ManagedMetricsConfig:
    resolved_api_key = api_key or os.environ.get("MIXPANEL_SERVICE_ACCOUNT_SECRET")
    if not resolved_api_key:
        raise RuntimeError("Missing MIXPANEL_SERVICE_ACCOUNT_SECRET")

    resolved_project_id = project_id or os.environ.get("MIXPANEL_PROJECT_ID")
    resolved_base_url = (base_url or os.environ.get("MIXPANEL_BASE_URL") or "https://eu.mixpanel.com").rstrip("/")
    resolved_timeout = timeout_seconds if timeout_seconds is not None else int(os.environ.get("MIXPANEL_TIMEOUT_SECONDS", "30"))
    return ManagedMetricsConfig(
        api_key=resolved_api_key,
        project_id=resolved_project_id,
        base_url=resolved_base_url,
        timeout_seconds=resolved_timeout,
    )


def build_managed_metrics_session(config: Optional[ManagedMetricsConfig] = None) -> requests.Session:
    cfg = config or load_managed_metrics_config()
    session = requests.Session()
    session.auth = (cfg.api_key, "")
    session.headers.update({"Accept": "application/json"})
    session.base_url = cfg.base_url  # type: ignore[attr-defined]
    session.timeout_seconds = cfg.timeout_seconds  # type: ignore[attr-defined]
    session.project_id = cfg.project_id  # type: ignore[attr-defined]
    return session


def get_managed_metrics_client(
    *,
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout_seconds: Optional[int] = None,
) -> requests.Session:
    config = load_managed_metrics_config(
        api_key=api_key,
        project_id=project_id,
        base_url=base_url,
        timeout_seconds=timeout_seconds,
    )
    return build_managed_metrics_session(config)
