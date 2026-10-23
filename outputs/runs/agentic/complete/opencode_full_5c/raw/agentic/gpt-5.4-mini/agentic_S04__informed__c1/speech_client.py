import os
from typing import Any, Dict, Optional


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


def get_api_key() -> str:
    key = os.getenv("ASSEMBLYAI_API_KEY")
    if not key:
        raise EnvironmentError("ASSEMBLYAI_API_KEY is required")
    return key


def get_headers() -> Dict[str, str]:
    return {"authorization": get_api_key(), "content-type": "application/json"}


def get_http_session() -> Any:
    import requests

    session = requests.Session()
    session.headers.update({"authorization": get_api_key()})
    return session


def post_json(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    import requests

    response = requests.post(
        f"{ASSEMBLYAI_API_BASE}{path}", headers=get_headers(), json=payload, timeout=60
    )
    response.raise_for_status()
    return response.json()


def get_json(path: str) -> Dict[str, Any]:
    import requests

    response = requests.get(
        f"{ASSEMBLYAI_API_BASE}{path}", headers=get_headers(), timeout=60
    )
    response.raise_for_status()
    return response.json()
