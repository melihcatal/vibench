import json
import os
import re
from typing import Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_json_object(text: str) -> Dict[str, str]:
    text = text.strip()
    try:
        data = json.loads(text)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return {}
        try:
            data = json.loads(match.group(0))
            return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}


def extract_key_values(document: str) -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "Extract all key-value pairs from the form-like document. "
        "Return only a JSON object mapping keys to string values. "
        "If a value appears multiple times, keep the most complete one.\n\n"
        f"Document:\n{document}"
    )
    payload = {
        "model": OPENAI_MODEL,
        "input": prompt,
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    text = ""
    if isinstance(data, dict):
        if "output_text" in data and isinstance(data["output_text"], str):
            text = data["output_text"]
        else:
            outputs = data.get("output", [])
            parts = []
            for item in outputs:
                for content in item.get("content", []):
                    if content.get("type") in {"output_text", "text"}:
                        parts.append(content.get("text", ""))
            text = "\n".join(parts)

    parsed = _extract_json_object(text)
    return {str(k): str(v) for k, v in parsed.items()}


if __name__ == "__main__":
    import sys

    doc = sys.stdin.read()
    print(json.dumps(extract_key_values(doc), ensure_ascii=False))
