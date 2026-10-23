import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_BASE = "https://api.openai.com/v1"
MICROSOFT_GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def get_config() -> Dict[str, str]:
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "microsoft_tenant_id": os.getenv("AZURE_TENANT_ID", ""),
        "microsoft_client_id": os.getenv("AZURE_CLIENT_ID", ""),
        "microsoft_client_secret": os.getenv("AZURE_CLIENT_SECRET", ""),
        "microsoft_graph_token": os.getenv("MICROSOFT_GRAPH_TOKEN", ""),
    }


def openai_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {get_config()['openai_api_key']}",
        "Content-Type": "application/json",
    }


def microsoft_headers() -> Dict[str, str]:
    token = get_config()["microsoft_graph_token"]
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def post_json(url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    response = requests.post(url, json=payload, headers=headers or {}, timeout=30)
    response.raise_for_status()
    return response.json()


def patch_json(url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    response = requests.patch(url, json=payload, headers=headers or {}, timeout=30)
    response.raise_for_status()
    if response.text:
        return response.json()
    return {}
