import json
import os
from typing import Any, Dict, Optional

import requests


ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.environ.get(name)
    return value if value else default


def _client_headers(api_key: str) -> Dict[str, str]:
    return {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }


def translate_runbook_notes(notes: str, target_language: str = "English", client: Optional[Any] = None) -> Dict[str, Any]:
    api_key = _env("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Missing API key; set ANTHROPIC_API_KEY")
    payload = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": f"Translate these secret-rotation runbook notes into {target_language}. Preserve meaning, commands, and checklist structure. Return only the translation.\n\n{notes}",
            }
        ],
    }
    if client is None:
        response = requests.post(ANTHROPIC_API_URL, headers=_client_headers(api_key), json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
    else:
        data = client.post(ANTHROPIC_API_URL, headers=_client_headers(api_key), json=payload).json()
    content = data.get("content", [])
    text = "".join(part.get("text", "") for part in content if isinstance(part, dict))
    return {
        "provider": "anthropic",
        "model": ANTHROPIC_MODEL,
        "target_language": target_language,
        "translation": text,
        "raw_response": data,
    }


def main() -> None:
    notes = _env("RUNBOOK_NOTES")
    if not notes:
        raise SystemExit("RUNBOOK_NOTES is required")
    target_language = _env("TARGET_LANGUAGE", "English")
    print(json.dumps(translate_runbook_notes(notes, target_language=target_language), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
