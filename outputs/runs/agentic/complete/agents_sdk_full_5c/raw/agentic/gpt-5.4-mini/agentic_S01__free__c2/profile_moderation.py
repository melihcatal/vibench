from __future__ import annotations

from typing import Any, Dict

import requests

from identity_client import get_identity_config, make_headers

OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def profile_moderation(profile_text: str) -> Dict[str, Any]:
    cfg = get_identity_config()
    resp = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={**make_headers(cfg), "Authorization": f"Bearer {cfg.client_secret}"},
        json={"model": OPENAI_MODERATION_MODEL, "input": profile_text},
        timeout=cfg.timeout_seconds,
    )
    resp.raise_for_status()
    data: Dict[str, Any] = resp.json() if resp.content else {}
    return data
