import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass(frozen=True)
class ObservabilityConfig:
    project_id: str
    api_key: str
    base_url: str = "https://api.datadoghq.com"
    site: str = "datadoghq.com"


def load_config() -> ObservabilityConfig:
    project_id = os.getenv("DATADOG_PROJECT_ID", "").strip()
    api_key = os.getenv("DD_API_KEY", os.getenv("DATADOG_API_KEY", "")).strip()
    base_url = os.getenv("DATADOG_API_URL", "https://api.datadoghq.com").strip() or "https://api.datadoghq.com"
    site = os.getenv("DATADOG_SITE", "datadoghq.com").strip() or "datadoghq.com"
    if not project_id:
        raise ValueError("DATADOG_PROJECT_ID is required")
    if not api_key:
        raise ValueError("DD_API_KEY or DATADOG_API_KEY is required")
    return ObservabilityConfig(project_id=project_id, api_key=api_key, base_url=base_url, site=site)


def create_session(config: Optional[ObservabilityConfig] = None) -> requests.Session:
    cfg = config or load_config()
    session = requests.Session()
    session.headers.update(
        {
            "DD-API-KEY": cfg.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )
    session.base_url = cfg.base_url  # type: ignore[attr-defined]
    session.project_id = cfg.project_id  # type: ignore[attr-defined]
    session.datadog_site = cfg.site  # type: ignore[attr-defined]
    return session


def api_url(path: str, config: Optional[ObservabilityConfig] = None) -> str:
    cfg = config or load_config()
    return f"{cfg.base_url.rstrip('/')}/{path.lstrip('/')}"
