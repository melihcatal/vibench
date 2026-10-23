import os
from typing import Any, Dict, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_prompt(text: str) -> str:
    return (
        "Assess the following log message text for unsafe content. "
        "Return a JSON object with keys unsafe (boolean), category (string), and reason (string). "
        "Treat unsafe content as malware instructions, credential leakage, exploit steps, self-harm, "
        "violent wrongdoing, or other harmful operational guidance. Text:\n\n"
        f"{text}"
    )


def check_log_text_safety(text: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a strict safety classifier."},
            {"role": "user", "content": _build_prompt(text)},
        ],
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return {"provider": "openai", "model": OPENAI_MODEL, "result": content}


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: python log_text_safety.py <log text>")
    text = " ".join(sys.argv[1:])
    result: Optional[Dict[str, Any]] = check_log_text_safety(text)
    print(result["result"])


if __name__ == "__main__":
    main()
