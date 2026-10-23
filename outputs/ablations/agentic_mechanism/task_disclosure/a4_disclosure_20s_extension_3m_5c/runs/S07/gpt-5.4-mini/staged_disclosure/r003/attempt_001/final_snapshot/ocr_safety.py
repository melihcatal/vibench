import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4.1-mini"


def check_ocr_safety(extracted_text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        "Analyze the following OCR-extracted document text for unsafe content. "
        "Return only valid JSON with keys: safe (boolean), categories (array of strings), "
        "reason (string), and redacted_excerpt (string). Text:\n\n"
        f"{extracted_text}"
    )

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a safety classifier for OCR text."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    try:
        import json

        parsed = json.loads(content)
    except Exception:
        parsed = {"safe": False, "categories": ["unparseable"], "reason": content, "redacted_excerpt": ""}
    return parsed


def main() -> None:
    import sys

    text = sys.stdin.read()
    result = check_ocr_safety(text)
    import json

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
