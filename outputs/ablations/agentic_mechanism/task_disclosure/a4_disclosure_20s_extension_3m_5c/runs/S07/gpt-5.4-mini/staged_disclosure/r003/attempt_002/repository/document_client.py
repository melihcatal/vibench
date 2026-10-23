import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
NOUCAT_API_URL = "https://api.nougat.cloud/v1/layout/extract"


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


def get_ocr_client() -> Dict[str, str]:
    return {"api_url": OPENAI_API_URL, "api_key": _require_env("OPENAI_API_KEY"), "model": "gpt-4o-mini"}


def get_layout_client() -> Dict[str, str]:
    return {"api_url": NOUCAT_API_URL, "api_key": _require_env("NOUCAT_API_KEY")}


def ocr_headers() -> Dict[str, str]:
    client = get_ocr_client()
    return {"Authorization": f"Bearer {client['api_key']}", "Content-Type": "application/json"}


def layout_headers() -> Dict[str, str]:
    client = get_layout_client()
    return {"Authorization": f"Bearer {client['api_key']}"}


def post_json(url: str, payload: Dict[str, Any], headers: Dict[str, str], timeout: int = 120) -> requests.Response:
    response = requests.post(url, json=payload, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response


def post_file(url: str, file_path: str, headers: Dict[str, str], data: Optional[Dict[str, Any]] = None, timeout: int = 120) -> requests.Response:
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        response = requests.post(url, headers=headers, files=files, data=data or {}, timeout=timeout)
    response.raise_for_status()
    return response
