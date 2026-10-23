import os
from typing import Any, Dict, Optional

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def get_perspective_api_key() -> str:
    return os.environ.get("PERSPECTIVE_API_KEY", "")


def perspective_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def perspective_params() -> Dict[str, str]:
    api_key = get_perspective_api_key()
    return {"key": api_key} if api_key else {}


def post_perspective(
    payload: Dict[str, Any], timeout: Optional[float] = 30.0
) -> Dict[str, Any]:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params=perspective_params(),
        headers=perspective_headers(),
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()
