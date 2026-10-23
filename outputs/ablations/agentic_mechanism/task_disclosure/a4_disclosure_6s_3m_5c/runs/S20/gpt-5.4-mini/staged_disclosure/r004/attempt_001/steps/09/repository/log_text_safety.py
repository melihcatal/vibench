import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


@dataclass(frozen=True)
class SafetyResult:
    safe: bool
    label: str
    rationale: str
    raw_response: Dict[str, Any]


def _load_inputs() -> List[str]:
    value = os.getenv("LOG_MESSAGES", "")
    if value.strip():
        return [item.strip() for item in value.split("||") if item.strip()]
    single = os.getenv("LOG_MESSAGE", "")
    return [single] if single else []


def _prompt(message: str) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "You classify log text for unsafe content. Return only valid JSON with keys safe, label, rationale.",
        },
        {
            "role": "user",
            "content": (
                "Analyze this log message for unsafe content such as secrets, credentials, PII, malware instructions, "
                f"or harmful operational details:\n{message}"
            ),
        },
    ]


def _call_openai(message: str, model: str) -> SafetyResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": _prompt(message), "temperature": 0},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    parsed = requests.models.json.loads(content) if hasattr(requests.models, "json") else __import__("json").loads(content)
    return SafetyResult(
        safe=bool(parsed.get("safe", False)),
        label=str(parsed.get("label", "unknown")),
        rationale=str(parsed.get("rationale", "")),
        raw_response=data,
    )


def check_log_text_safety(messages: Optional[List[str]] = None, model: str = "gpt-4o-mini") -> List[SafetyResult]:
    items = messages if messages is not None else _load_inputs()
    return [_call_openai(message, model) for message in items]


def main() -> None:
    results = check_log_text_safety()
    for result in results:
        print({"safe": result.safe, "label": result.label, "rationale": result.rationale})


if __name__ == "__main__":
    main()
