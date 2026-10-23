import os
import requests
from typing import Dict, Any


def get_api_key(key_name: str) -> str:
    key = os.getenv(key_name)
    if not key:
        raise ValueError(f"Missing environment variable: {key_name}")
    return key


def post_to_api(
    url: str, payload: Dict[str, Any], api_key: str, key_is_query: bool = False
) -> Dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    if key_is_query:
        url += f"?key={api_key}"
    else:
        headers["Authorization"] = f"Bearer {api_key}"
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
