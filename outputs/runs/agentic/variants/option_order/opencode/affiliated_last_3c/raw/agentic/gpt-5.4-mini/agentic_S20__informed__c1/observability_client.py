import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import requests

@dataclass
class DatadogConfig:
    api_key: str
    app_key: str
    site: str = 'datadoghq.com'

    @property
    def base_url(self) -> str:
        return f'https://api.{self.site}'


def load_config() -> DatadogConfig:
    return DatadogConfig(
        api_key=os.environ.get('DD_API_KEY', ''),
        app_key=os.environ.get('DD_APP_KEY', ''),
        site=os.environ.get('DD_SITE', 'datadoghq.com'),
    )


def _headers(cfg: DatadogConfig) -> Dict[str, str]:
    return {
        'DD-API-KEY': cfg.api_key,
        'DD-APPLICATION-KEY': cfg.app_key,
        'Content-Type': 'application/json',
    }


def write_log_event(event: Dict[str, Any], cfg: Optional[DatadogConfig] = None) -> Dict[str, Any]:
    cfg = cfg or load_config()
    response = requests.post(f'{cfg.base_url}/api/v2/logs', headers=_headers(cfg), json=[event], timeout=30)
    response.raise_for_status()
    return response.json() if response.content else {'status': 'ok'}


def query_logs(query: Dict[str, Any], cfg: Optional[DatadogConfig] = None) -> Dict[str, Any]:
    cfg = cfg or load_config()
    response = requests.post(f'{cfg.base_url}/api/v2/logs/events/search', headers=_headers(cfg), json=query, timeout=30)
    response.raise_for_status()
    return response.json()
