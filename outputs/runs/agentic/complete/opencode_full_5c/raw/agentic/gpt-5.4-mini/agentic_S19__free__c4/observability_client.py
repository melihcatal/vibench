import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class ObservabilityConfig:
    datadog_api_key: Optional[str]
    datadog_app_key: Optional[str]
    datadog_site: str
    openai_api_key: Optional[str]
    azure_storage_connection_string: Optional[str]
    azure_storage_account_url: Optional[str]


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        datadog_api_key=os.getenv("DATADOG_API_KEY"),
        datadog_app_key=os.getenv("DATADOG_APP_KEY"),
        datadog_site=os.getenv("DATADOG_SITE", "datadoghq.com"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        azure_storage_connection_string=os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
        azure_storage_account_url=os.getenv("AZURE_STORAGE_ACCOUNT_URL"),
    )


def datadog_session(config: Optional[ObservabilityConfig] = None) -> requests.Session:
    cfg = config or load_config()
    session = requests.Session()
    if cfg.datadog_api_key:
        session.headers["DD-API-KEY"] = cfg.datadog_api_key
    if cfg.datadog_app_key:
        session.headers["DD-APPLICATION-KEY"] = cfg.datadog_app_key
    return session


def datadog_base_url(config: Optional[ObservabilityConfig] = None) -> str:
    cfg = config or load_config()
    return f"https://api.{cfg.datadog_site}"
