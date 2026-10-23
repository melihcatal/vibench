import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


MODEL_ID = os.getenv("OPENAI_INVOICE_MODEL", "gpt-4.1-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def _response_text(response: Any) -> str:
    text = getattr(response, "output_text", None)
    if isinstance(text, str) and text.strip():
        return text
    parts: List[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            value = getattr(content, "text", None)
            if isinstance(value, str):
                parts.append(value)
    return "".join(parts)


def _safe_json_loads(text: str) -> Dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].lstrip()
    return json.loads(text)


def extract_invoice_fields(invoice_text: str) -> Dict[str, Any]:
    prompt = (
        "Extract structured invoice fields as JSON with keys vendor, date, total, and line_items. "
        "line_items must be an array of objects with description, quantity, unit_price, and amount when available. "
        "Return only valid JSON. Invoice text:\n\n"
        f"{invoice_text}"
    )
    response = _client().responses.create(
        model=MODEL_ID,
        input=prompt,
        temperature=0,
    )
    content = _response_text(response)
    return _safe_json_loads(content)


def main() -> None:
    import sys

    invoice_text = sys.stdin.read()
    result = extract_invoice_fields(invoice_text)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
