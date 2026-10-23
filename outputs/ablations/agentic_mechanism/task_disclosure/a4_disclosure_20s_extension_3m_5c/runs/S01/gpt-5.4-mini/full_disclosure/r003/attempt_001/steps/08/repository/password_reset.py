import os
from typing import Any, Dict, Optional

import requests


STRIPE_IDENTITY_API_BASE = "https://identity.stripe.com"


def start_password_reset(email: str, return_url: Optional[str] = None, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.environ.get("STRIPE_SECRET_KEY") or os.environ.get("STRIPE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing STRIPE_SECRET_KEY or STRIPE_API_KEY")

    payload = {"email": email}
    if return_url:
        payload["return_url"] = return_url

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key

    response = requests.post(f"{STRIPE_IDENTITY_API_BASE}/v1/password_resets", json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
