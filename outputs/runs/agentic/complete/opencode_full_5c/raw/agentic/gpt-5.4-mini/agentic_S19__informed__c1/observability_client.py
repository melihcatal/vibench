import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class ObservabilityConfig:
    base_url: str
    api_key: str
    app_key: str
    timeout: int = 30


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        base_url=os.getenv("DD_SITE", "https://api.datadoghq.com"),
        api_key=os.environ["DD_API_KEY"],
        app_key=os.environ["DD_APP_KEY"],
        timeout=int(os.getenv("OBSERVABILITY_TIMEOUT", "30")),
    )


def build_session(config: Optional[ObservabilityConfig] = None) -> requests.Session:
    config = config or load_config()
    session = requests.Session()
    session.headers.update(
        {
            "DD-API-KEY": config.api_key,
            "DD-APPLICATION-KEY": config.app_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    )
    session.base_url = config.base_url  # type: ignore[attr-defined]
    session.timeout = config.timeout  # type: ignore[attr-defined]
    return session


def get_json(
    path: str,
    params: Optional[Dict[str, Any]] = None,
    config: Optional[ObservabilityConfig] = None,
) -> Dict[str, Any]:
    config = config or load_config()
    session = build_session(config)
    response = session.get(
        f"{config.base_url}{path}", params=params, timeout=config.timeout
    )
    response.raise_for_status()
    return response.json()
