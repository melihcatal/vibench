import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class ObservabilityConfig:
    api_key: str
    base_url: str = "https://api.datadoghq.com"
    site: str = "datadoghq.com"
    timeout: float = 30.0


def load_config() -> ObservabilityConfig:
    api_key = os.getenv("DATADOG_API_KEY") or os.getenv("DD_API_KEY")
    if not api_key:
        raise ValueError("DATADOG_API_KEY is required")
    base_url = os.getenv("DATADOG_API_URL") or f"https://api.{os.getenv('DATADOG_SITE', 'datadoghq.com')}"
    site = os.getenv("DATADOG_SITE", "datadoghq.com")
    timeout = float(os.getenv("OBSERVABILITY_TIMEOUT_SECONDS", "30"))
    return ObservabilityConfig(api_key=api_key, base_url=base_url.rstrip("/"), site=site, timeout=timeout)


class ObservabilityClient:
    def __init__(self, config: Optional[ObservabilityConfig] = None) -> None:
        self.config = config or load_config()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "DD-API-KEY": self.config.api_key,
                "Content-Type": "application/json",
            }
        )

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.config.base_url}{path}"
        timeout = kwargs.pop("timeout", self.config.timeout)
        response = self.session.request(method, url, timeout=timeout, **kwargs)
        response.raise_for_status()
        return response

    def get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.request("GET", path, params=params).json()

    def post_json(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.request("POST", path, json=payload).json()


def create_client(config: Optional[ObservabilityConfig] = None) -> ObservabilityClient:
    return ObservabilityClient(config=config)
