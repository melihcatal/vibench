import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _messages_from_prompt(prompt: str) -> List[Dict[str, str]]:
    return [{"role": "user", "content": prompt}]


def collect_platform_metadata(prompt: str, model: str = OPENAI_MODEL) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": _messages_from_prompt(prompt),
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()

    choice = payload["choices"][0]
    message = choice.get("message", {})

    return {
        "provider": "openai",
        "model": payload.get("model", model),
        "resource_id": payload.get("id"),
        "output": message.get("content"),
        "usage": payload.get("usage"),
        "finish_reason": choice.get("finish_reason"),
        "model_handle": model,
        "raw": payload,
    }


def main() -> None:
    prompt = os.environ.get("PROMPT", "Hello")
    result = collect_platform_metadata(prompt)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
