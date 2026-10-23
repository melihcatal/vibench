import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def extract_key_values(document_text: str, schema_hint: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt_parts: List[str] = [
        "Extract key-value pairs from the following form-like document text.",
        "Return JSON with a top-level object containing a 'key_values' array.",
        "Each array item must have 'key', 'value', and optionally 'confidence'.",
        "Preserve field names as written when possible.",
    ]
    if schema_hint:
        prompt_parts.append(f"Schema hint: {schema_hint}")
    prompt_parts.append(f"Document text:\n{document_text}")

    payload = {
        "model": OPENAI_MODEL,
        "input": [{"role": "user", "content": [{"type": "input_text", "text": "\n".join(prompt_parts)}]}],
        "response_format": {"type": "json_object"},
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

    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                output_text += content.get("text", "")

    if not output_text and isinstance(data.get("output_text"), str):
        output_text = data["output_text"]

    if not output_text:
        return {"key_values": []}

    parsed = requests.utils.json.loads(output_text)
    if isinstance(parsed, dict) and "key_values" in parsed:
        return parsed
    return {"key_values": parsed if isinstance(parsed, list) else []}
