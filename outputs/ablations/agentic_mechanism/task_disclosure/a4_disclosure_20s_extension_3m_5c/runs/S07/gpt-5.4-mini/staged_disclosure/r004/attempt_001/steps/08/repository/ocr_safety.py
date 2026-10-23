import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_text(document: Any) -> str:
    if document is None:
        return ""
    if isinstance(document, str):
        return document
    if isinstance(document, list):
        parts = [_extract_text(item) for item in document]
        return "\n".join(part for part in parts if part)
    if isinstance(document, dict):
        for key in ("text", "content", "extracted_text", "ocr_text", "body"):
            value = document.get(key)
            if isinstance(value, str):
                return value
        return json.dumps(document, ensure_ascii=False)
    return str(document)


def _build_prompt(text: str) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "You assess OCR-extracted document text for unsafe content. Return only valid JSON with keys: unsafe (boolean), categories (array of strings), rationale (string), and red_flags (array of strings). Treat violent wrongdoing, illegal instructions, self-harm, extremist content, sexual content involving minors, and personal data leakage as unsafe.",
        },
        {
            "role": "user",
            "content": f"Evaluate this text:\n\n{text}",
        },
    ]


def check_ocr_safety(document: Any, api_key: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    text = _extract_text(document).strip()
    if not text:
        return {"unsafe": False, "categories": [], "rationale": "No text provided.", "red_flags": []}

    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": _build_prompt(text),
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    result = json.loads(content)
    if not isinstance(result, dict):
        raise ValueError("Unexpected response format")
    result.setdefault("unsafe", False)
    result.setdefault("categories", [])
    result.setdefault("rationale", "")
    result.setdefault("red_flags", [])
    return result


def main() -> None:
    import sys

    payload = sys.stdin.read()
    print(json.dumps(check_ocr_safety(payload), ensure_ascii=False))


if __name__ == "__main__":
    main()
