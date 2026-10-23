import json
import os
import re
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_text(data: Any) -> str:
    if isinstance(data, str):
        return data
    if not isinstance(data, dict):
        return ""
    if isinstance(data.get("output_text"), str):
        return data["output_text"]
    parts: List[str] = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                parts.append(str(content.get("text", "")))
    return "\n".join(parts)


def _extract_json_object(text: str) -> Dict[str, Any]:
    text = text.strip()
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return {}
        try:
            parsed = json.loads(match.group(0))
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return {}


def _normalize_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key, value in payload.items():
        if value is None:
            continue
        if isinstance(value, (dict, list, bool, int, float)):
            normalized[str(key)] = value
        else:
            normalized[str(key)] = str(value)
    return normalized


def extract_document_fields(document_text: str, field_names: Optional[List[str]] = None) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    fields_hint = ""
    if field_names:
        fields_hint = "Target fields: " + ", ".join(field_names) + "\n\n"

    prompt = (
        "Extract structured fields from the OCR-normalized document text. "
        "Return only a JSON object. Use null for missing values. "
        "Preserve dates, amounts, names, IDs, and addresses as they appear when possible.\n\n"
        f"{fields_hint}Document:\n{document_text}"
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": prompt,
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return _normalize_fields(_extract_json_object(_extract_text(data)))


if __name__ == "__main__":
    import sys

    print(json.dumps(extract_document_fields(sys.stdin.read()), ensure_ascii=False))
