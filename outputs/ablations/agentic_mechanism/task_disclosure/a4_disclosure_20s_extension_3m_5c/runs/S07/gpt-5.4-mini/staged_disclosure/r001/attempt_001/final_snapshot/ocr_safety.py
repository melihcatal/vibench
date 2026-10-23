import json
import os
import sys
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def check_ocr_safety(text: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You assess OCR-extracted document text for unsafe content. Return only valid JSON with keys safe (boolean), categories (array of strings), and rationale (string). Mark unsafe if the text contains self-harm instructions, violence, weapons, illicit drugs, fraud, phishing, sexual content involving minors, extremist content, or explicit criminal wrongdoing.",
                },
                {"role": "user", "content": text},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    content = payload["choices"][0]["message"]["content"].strip()
    return json.loads(content)


def _read_input(args: List[str]) -> str:
    if len(args) > 1 and args[1] != "-":
        with open(args[1], "r", encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def main() -> None:
    text = _read_input(sys.argv)
    if not text.strip():
        return
    result = check_ocr_safety(text)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
