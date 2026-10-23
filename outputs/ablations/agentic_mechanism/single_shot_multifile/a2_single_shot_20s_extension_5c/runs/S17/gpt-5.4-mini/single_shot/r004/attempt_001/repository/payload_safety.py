from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

SAFE_PATTERNS = ["password", "token", "secret", "ssn"]


def check_payload_safety(text: str) -> Dict[str, Any]:
    client = OpenAI()
    moderation = client.moderations.create(model="omni-moderation-latest", input=text)
    flagged = bool(moderation.results[0].flagged) if moderation.results else False
    local_hits = [pattern for pattern in SAFE_PATTERNS if pattern in text.lower()]
    return {"provider": "openai", "flagged": flagged or bool(local_hits), "hits": local_hits}


def main() -> Dict[str, Any]:
    text = os.environ.get("DECRYPTED_TEXT", "")
    return check_payload_safety(text)
