import os
from dataclasses import dataclass


@dataclass
class ObservabilityConfig:
    site: str
    api_key: str
    app_key: str


def load_observability_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        site=os.getenv("DD_SITE", "datadoghq.com"),
        api_key=os.getenv("DD_API_KEY", ""),
        app_key=os.getenv("DD_APP_KEY", ""),
    )


def datadog_headers(config: ObservabilityConfig) -> dict:
    return {
        "DD-API-KEY": config.api_key,
        "DD-APPLICATION-KEY": config.app_key,
        "Content-Type": "application/json",
    }


def datadog_base_url(config: ObservabilityConfig) -> str:
    return f"https://api.{config.site}"
