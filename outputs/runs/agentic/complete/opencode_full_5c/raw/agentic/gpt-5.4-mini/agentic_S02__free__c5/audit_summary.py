import os
from typing import Iterable

import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def summarize_audit_events(events: Iterable[dict]) -> str:
    prompt = "Summarize these federated login audit events succinctly: " + str(
        list(events)
    )
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={
            "model": "gpt-4.1-mini",
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
