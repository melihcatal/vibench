import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_text(receipt_input: Any) -> str:
    if receipt_input is None:
        return ""
    if isinstance(receipt_input, str):
        return receipt_input.strip()
    if isinstance(receipt_input, bytes):
        return receipt_input.decode("utf-8", errors="ignore").strip()
    if isinstance(receipt_input, dict):
        return json.dumps(receipt_input, ensure_ascii=False)
    return str(receipt_input).strip()


def extract_receipt_fields(receipt_input: Any, api_key: Optional[str] = None, timeout: int = 60) -> Dict[str, Any]:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        "Extract structured receipt fields as JSON with keys merchant, tax, total, and items. "
        "items must be an array of objects with name, quantity, unit_price, and total fields when available. "
        "Return only valid JSON. Receipt text:\n"
        + _extract_text(receipt_input)
    )

    payload = {
        "model": OPENAI_MODEL,
        "input": prompt,
        "temperature": 0,
    }

    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()

    text = ""
    if isinstance(data, dict):
        output = data.get("output", [])
        for item in output:
            if isinstance(item, dict):
                content = item.get("content", [])
                for chunk in content:
                    if isinstance(chunk, dict):
                        if chunk.get("type") in {"output_text", "text"} and "text" in chunk:
                            text += chunk["text"]
        if not text and "output_text" in data:
            text = data["output_text"] if isinstance(data["output_text"], str) else json.dumps(data["output_text"])

    parsed: Dict[str, Any]
    try:
        parsed = json.loads(text)
    except Exception:
        parsed = {"merchant": None, "tax": None, "total": None, "items": [], "raw": text}

    parsed.setdefault("merchant", None)
    parsed.setdefault("tax", None)
    parsed.setdefault("total", None)
    parsed.setdefault("items", [])
    return parsed


__all__ = ["extract_receipt_fields"]
