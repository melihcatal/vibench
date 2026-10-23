import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def moderate_claims(text: str, api_key: Optional[str] = None, timeout: float = 30.0) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        "Moderate the following free-text claims or notes for policy risks. "
        "Return strict JSON with keys: allowed (boolean), categories (array of strings), "
        "risk_level (string), rationale (string), redacted_text (string). Text: "
        + text
    )

    payload = {
        "model": OPENAI_MODEL,
        "input": prompt,
        "temperature": 0,
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(payload), timeout=timeout)
    response.raise_for_status()
    data = response.json()

    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                output_text += content.get("text", "")

    if not output_text:
        raise ValueError("No moderation response text returned")

    return json.loads(output_text)
