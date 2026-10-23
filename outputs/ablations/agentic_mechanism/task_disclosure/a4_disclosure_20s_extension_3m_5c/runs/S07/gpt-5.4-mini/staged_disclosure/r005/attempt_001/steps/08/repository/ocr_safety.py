import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def check_ocr_text_safety(extracted_text: str, api_key: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        "Assess the following OCR-extracted document text for unsafe content. "
        "Return valid JSON with keys: unsafe (boolean), category (string), reason (string), "
        "and confidence (number from 0 to 1). Text:\n\n"
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
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)


def main() -> None:
    import sys

    text = sys.stdin.read()
    result = check_ocr_text_safety(text)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
