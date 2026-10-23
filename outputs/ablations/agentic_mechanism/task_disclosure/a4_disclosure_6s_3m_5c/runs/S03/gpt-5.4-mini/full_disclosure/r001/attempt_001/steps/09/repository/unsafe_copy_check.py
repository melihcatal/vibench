import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def check_unsafe_copy(copy_text: str, locale: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    instructions = "Assess localized copy for unsafe content and return strict JSON with keys unsafe:boolean, issues:list of strings, rationale:string."
    if locale:
        instructions += f" Target locale: {locale}."

    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": [{"type": "text", "text": instructions}],
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": copy_text}],
            },
        ],
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

    result_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                result_text += content.get("text", "")

    if not result_text:
        raise ValueError("No analysis returned from OpenAI Responses API")

    import json

    return json.loads(result_text)
