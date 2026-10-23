from __future__ import annotations

from typing import Any, Dict

import requests

TISANE_ENDPOINT = "https://api.tisane.ai/parse"


def vendor_text_safety(text: str) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {__import__('os').environ.get('TISANE_API_KEY', '')}"}
    payload = {"content": text, "language": "en", "snippets": True}
    response = requests.post(TISANE_ENDPOINT, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
