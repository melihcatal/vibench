import os
from typing import Any, Dict


def get_config() -> Dict[str, str]:
    return {
        "azure_connection_string": os.environ.get("AZURE_SERVICE_BUS_CONNECTION_STRING", ""),
        "azure_queue_name": os.environ.get("AZURE_SERVICE_BUS_QUEUE_NAME", ""),
        "azure_dead_letter_queue": os.environ.get("AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE", ""),
        "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
        "openai_model": os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        "openai_endpoint": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    }


def require(value: str, name: str) -> str:
    if not value:
        raise ValueError(f"missing {name}")
    return value


def json_headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
