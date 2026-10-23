from __future__ import annotations

from observability_client import load_config


def log_message_translate(message: str, target_locale: str = "es") -> str:
    import requests

    cfg = load_config()
    headers = {"Authorization": f"Bearer {cfg.api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": f"Translate support-visible log messages into {target_locale}."},
            {"role": "user", "content": message},
        ],
        "temperature": 0.1,
    }
    resp = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
