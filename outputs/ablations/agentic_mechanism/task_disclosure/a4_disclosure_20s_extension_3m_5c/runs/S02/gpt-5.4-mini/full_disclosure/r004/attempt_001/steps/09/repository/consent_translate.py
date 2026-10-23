import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_consent_copy(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    instructions = [
        "Translate identity-provider consent copy for an OAuth/OIDC login flow.",
        "Preserve meaning, tone, labels, placeholders, line breaks, product names, and legal/regulatory terms.",
        "Return only the translated text.",
    ]
    if source_language:
        instructions.append(f"Source language: {source_language}.")
    instructions.append(f"Target language: {target_language}.")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": [{"type": "text", "text": " ".join(instructions)}],
            },
            {"role": "user", "content": [{"type": "text", "text": text}]},
        ],
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

    output_text = _extract_output_text(data)
    if not output_text:
        raise RuntimeError("No translation returned by OpenAI Responses API")
    return output_text.strip()


def _extract_output_text(data: Dict[str, Any]) -> str:
    output = data.get("output", [])
    parts: List[str] = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                parts.append(content["text"])
    if parts:
        return "".join(parts)
    return data.get("output_text", "") or ""
