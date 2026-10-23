import os
import requests

TISANE_API_KEY = os.getenv("TISANE_API_KEY")


def redact_unsafe(text: str) -> str:
    if not TISANE_API_KEY:
        return text  # No-op if no key

    url = "https://api.tisane.ai/analyze"
    headers = {
        "Authorization": f"Bearer {TISANE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "content": text,
        "language": "en",
        "settings": {"profiles": ["abuse-allegations"]},
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        return text

    data = response.json()
    spans = data.get("content_spans", [])
    spans.sort(key=lambda x: x.get("begin", 0), reverse=True)

    redacted = text
    for span in spans:
        flags = span.get("flags", [])
        if flags:
            start = span["begin"]
            end = span["end"]
            redacted = redacted[:start] + "[REDACTED]" + redacted[end:]

    return redacted
