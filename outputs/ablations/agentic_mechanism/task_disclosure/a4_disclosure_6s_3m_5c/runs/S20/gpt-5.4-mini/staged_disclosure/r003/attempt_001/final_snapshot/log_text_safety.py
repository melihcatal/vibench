import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_RESPONSES_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL_ID = "gpt-5.4-mini"


def _build_prompt(text: str) -> str:
    return (
        "You are a log text safety classifier. Evaluate the provided log message text for unsafe content. "
        "Return strict JSON with keys: unsafe (boolean), categories (array of strings), reason (string), "
        "redacted_text (string). Categories should include any of: malware, phishing, credential_theft, "
        "personal_data, self_harm, violence, hate, sexual_content, fraud, illegal_activity, other. "
        "If the text is safe, set unsafe to false, categories to an empty array, and reason to a brief explanation.\n\n"
        f"Log text:\n{text}"
    )


def check_log_text_safety(text: str, api_key: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL_ID,
        "input": [
            {
                "role": "user",
                "content": [{"type": "text", "text": _build_prompt(text)}],
            }
        ],
        "text": {"format": {"type": "json_object"}},
    }

    response = requests.post(
        OPENAI_RESPONSES_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()

    text_output = ""
    output_items = data.get("output", [])
    for item in output_items:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text_output += content.get("text", "")

    if not text_output and "output_text" in data:
        text_output = data["output_text"]

    if not text_output:
        return {"unsafe": True, "categories": ["other"], "reason": "No classification returned", "raw": data}

    try:
        result = json.loads(text_output)
    except json.JSONDecodeError:
        return {"unsafe": True, "categories": ["other"], "reason": "Invalid JSON returned", "raw": data}

    if not isinstance(result, dict):
        return {"unsafe": True, "categories": ["other"], "reason": "Unexpected response shape", "raw": data}

    result.setdefault("unsafe", True)
    result.setdefault("categories", ["other"])
    result.setdefault("reason", "Missing fields in response")
    result.setdefault("redacted_text", "")
    return result


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Check selected log message text for unsafe content")
    parser.add_argument("text", help="Log message text to evaluate")
    parser.add_argument("--api-key", dest="api_key", default=None)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    print(json.dumps(check_log_text_safety(args.text, api_key=args.api_key, timeout=args.timeout), ensure_ascii=False))


if __name__ == "__main__":
    main()
