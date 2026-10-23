from __future__ import annotations

from typing import Dict

from observability_client import load_config


def log_text_safety(message: str) -> Dict[str, object]:
    import requests

    cfg = load_config()
    headers = {"Authorization": f"Bearer {cfg.api_key}"}
    payload = {"model": "omni-moderation-latest", "input": message}
    resp = requests.post("https://api.openai.com/v1/moderations", json=payload, headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return {"provider": "openai", "raw": data}
