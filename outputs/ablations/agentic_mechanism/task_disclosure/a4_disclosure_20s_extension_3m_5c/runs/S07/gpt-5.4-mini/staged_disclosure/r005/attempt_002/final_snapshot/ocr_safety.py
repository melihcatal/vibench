import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_prompt(text: str) -> str:
    return (
        "You are a document safety classifier. Analyze the extracted document text "
        "and return strict JSON with keys unsafe (boolean), categories (array of strings), "
        "and rationale (string). Flag unsafe content including violence, self-harm, hate, "
        "sexual content, illicit behavior, or explicit instructions to cause harm. "
        "If the text is safe, set unsafe to false and categories to an empty array. "
        "Document text:\n" + text
    )


def check_ocr_safety(text: str, api_key: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": "Return only valid JSON."}],
            },
            {"role": "user", "content": [{"type": "input_text", "text": _build_prompt(text)}]},
        ],
    }

    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()

    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                output_text += content.get("text", "")

    if not output_text:
        raise ValueError("No model output received")

    return json.loads(output_text)
