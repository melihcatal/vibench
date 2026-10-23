from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from security_models import NormalizedEvent, normalize_event


MODEL_ID = "gpt-4o-mini"


def summarize_key_usage(events: Iterable[dict]) -> str:
    client = OpenAI()
    normalized = [normalize_event(e) for e in events]
    prompt = "Summarize key usage and crypto events:\n" + "\n".join(f"{e.timestamp or ''} {e.actor} {e.action} {e.key_id}" for e in normalized)
    response = client.chat.completions.create(model=MODEL_ID, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    pass
