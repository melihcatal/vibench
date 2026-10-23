import json
import os
import re
import sys
from typing import Dict, List, Tuple

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _fallback_extract(text: str) -> Dict[str, str]:
    pairs: Dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        match = re.match(r"^\s*([^:={\n]+?)\s*[:=]\s*(.+?)\s*$", line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            if key and value:
                pairs[key] = value
    return pairs


def _build_messages(text: str) -> List[Dict[str, str]]:
    system = "Extract key-value pairs from the provided form-like document. Return only valid JSON object data."
    user = f"Document:\n{text}\n\nReturn a JSON object of extracted key-value pairs."
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def extract_key_values(text: str) -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _fallback_extract(text)

    payload = {
        "model": OPENAI_MODEL,
        "messages": _build_messages(text),
        "temperature": 0,
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
    content = data["choices"][0]["message"]["content"]
    try:
        parsed = json.loads(content)
        if isinstance(parsed, dict):
            return {str(k): str(v) for k, v in parsed.items()}
    except json.JSONDecodeError:
        pass
    return _fallback_extract(content)


def main() -> None:
    input_text = sys.stdin.read()
    result = extract_key_values(input_text)
    sys.stdout.write(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
