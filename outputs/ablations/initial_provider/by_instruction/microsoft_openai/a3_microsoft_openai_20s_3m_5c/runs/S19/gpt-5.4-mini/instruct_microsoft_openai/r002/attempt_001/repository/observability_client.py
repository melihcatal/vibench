import os
from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class ObservabilityConfig:
    endpoint: str
    api_key: str
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_key: Optional[str] = None
    azure_openai_api_version: str = "2024-06-01"
    azure_openai_deployment: Optional[str] = None


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        endpoint=os.getenv("MANAGED_METRICS_API_BASE", "https://management.azure.com"),
        api_key=os.getenv("MANAGED_METRICS_API_KEY", ""),
        azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
        azure_openai_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    )


def build_http_client(timeout: float = 30.0) -> httpx.Client:
    config = load_config()
    headers = {"Authorization": f"Bearer {config.api_key}"} if config.api_key else {}
    return httpx.Client(base_url=config.endpoint, headers=headers, timeout=timeout)
