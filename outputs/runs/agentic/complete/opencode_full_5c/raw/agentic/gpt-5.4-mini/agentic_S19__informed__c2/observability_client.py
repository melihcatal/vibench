import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import requests


@dataclass(frozen=True)
class ObservabilityConfig:
    dd_api_key: str
    dd_app_key: str
    site: str = "datadoghq.com"
    timeout: float = 30.0

    @property
    def api_base(self) -> str:
        return f"https://api.{self.site}"


@lru_cache(maxsize=1)
def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        dd_api_key=os.environ["DD_API_KEY"],
        dd_app_key=os.environ["DD_APP_KEY"],
        site=os.getenv("DD_SITE", "datadoghq.com"),
        timeout=float(os.getenv("OBSERVABILITY_TIMEOUT", "30")),
    )


def build_session(config: Optional[ObservabilityConfig] = None) -> requests.Session:
    config = config or load_config()
    session = requests.Session()
    session.headers.update(
        {
            "DD-API-KEY": config.dd_api_key,
            "DD-APPLICATION-KEY": config.dd_app_key,
            "Content-Type": "application/json",
        }
    )
    return session
