import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_payload_text(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, bytes):
        return payload.decode("utf-8", errors="replace")
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def check_decrypted_payload_safety(payload: Any, api_key: Optional[str] = None) -> Dict[str, Any]:
    text = _extract_payload_text(payload)
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "You are a payload safety classifier. Decide whether decrypted text contains unsafe content. Return strict JSON with fields unsafe:boolean, category:string, reason:string, confidence:number.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": text,
                        }
                    ],
                },
            ],
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                output_text += content.get("text", "")
    if not output_text:
        output_text = json.dumps(data, ensure_ascii=False)
    try:
        return json.loads(output_text)
    except json.JSONDecodeError:
        return {
            "unsafe": True,
            "category": "unparseable",
            "reason": output_text,
            "confidence": 0.0,
        }
