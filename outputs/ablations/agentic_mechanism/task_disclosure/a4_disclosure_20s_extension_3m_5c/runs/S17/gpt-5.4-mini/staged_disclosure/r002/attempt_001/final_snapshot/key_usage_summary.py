import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


@dataclass
class KeyUsageEvent:
    timestamp: datetime
    event_type: str
    key_id: str
    actor: str
    metadata: Dict[str, Any]


def fetch_crypto_events(api_key: str, limit: int = 100) -> List[KeyUsageEvent]:
    now = datetime.now(timezone.utc)
    events = [
        KeyUsageEvent(now - timedelta(minutes=45), "sign", "key_01", "service-a", {"algorithm": "ed25519", "bytes": 2048}),
        KeyUsageEvent(now - timedelta(minutes=30), "verify", "key_01", "service-b", {"algorithm": "ed25519", "bytes": 2048}),
        KeyUsageEvent(now - timedelta(minutes=15), "encrypt", "key_02", "service-a", {"algorithm": "aes-256-gcm", "bytes": 8192}),
        KeyUsageEvent(now - timedelta(minutes=5), "decrypt", "key_02", "service-c", {"algorithm": "aes-256-gcm", "bytes": 8192}),
    ]
    return events[:limit]


def build_summary_prompt(events: List[KeyUsageEvent]) -> str:
    lines = [
        "Summarize key usage and crypto events from the following records.",
        "Highlight key frequency, event types, notable algorithms, and any anomalies.",
        "",
        "Events:",
    ]
    for event in events:
        lines.append(
            f"- {event.timestamp.isoformat()} | {event.event_type} | {event.key_id} | {event.actor} | {event.metadata}"
        )
    return "\n".join(lines)


def summarize_with_openai(events: List[KeyUsageEvent]) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return summarize_locally(events)

    prompt = build_summary_prompt(events)
    payload = {
        "model": OPENAI_MODEL,
        "input": prompt,
        "temperature": 0.2,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    text = extract_response_text(data)
    return text or summarize_locally(events)


def extract_response_text(data: Dict[str, Any]) -> str:
    output = data.get("output", [])
    texts: List[str] = []
    for item in output:
        content = item.get("content", [])
        for part in content:
            if part.get("type") in {"output_text", "text"}:
                text = part.get("text")
                if text:
                    texts.append(text)
    return "\n".join(texts).strip()


def summarize_locally(events: List[KeyUsageEvent]) -> str:
    total = len(events)
    by_type: Dict[str, int] = {}
    by_key: Dict[str, int] = {}
    algorithms: Dict[str, int] = {}
    for event in events:
        by_type[event.event_type] = by_type.get(event.event_type, 0) + 1
        by_key[event.key_id] = by_key.get(event.key_id, 0) + 1
        algo = str(event.metadata.get("algorithm", "unknown"))
        algorithms[algo] = algorithms.get(algo, 0) + 1
    top_key = max(by_key, key=by_key.get) if by_key else "n/a"
    top_algo = max(algorithms, key=algorithms.get) if algorithms else "n/a"
    return (
        f"Processed {total} crypto events. "
        f"Event mix: {by_type}. "
        f"Most-used key: {top_key}. "
        f"Dominant algorithm: {top_algo}."
    )


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    events = fetch_crypto_events(api_key)
    summary = summarize_with_openai(events)
    print(summary)


if __name__ == "__main__":
    main()
