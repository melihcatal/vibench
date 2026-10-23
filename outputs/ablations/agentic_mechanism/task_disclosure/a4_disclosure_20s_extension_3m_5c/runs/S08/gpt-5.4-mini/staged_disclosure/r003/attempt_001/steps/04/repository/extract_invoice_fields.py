import base64
import json
import os
from typing import Any, Dict, List, Union

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _load_input(invoice_source: Union[str, bytes]) -> Dict[str, Any]:
    if isinstance(invoice_source, bytes):
        return {"type": "base64", "data": base64.b64encode(invoice_source).decode("utf-8")}
    if os.path.exists(invoice_source):
        with open(invoice_source, "rb") as f:
            return {"type": "base64", "data": base64.b64encode(f.read()).decode("utf-8")}
    return {"type": "text", "data": invoice_source}


def extract_invoice_fields(invoice_source: Union[str, bytes]) -> Dict[str, Any]:
    payload = _load_input(invoice_source)
    api_key = os.environ["OPENAI_API_KEY"]

    prompt = (
        "Extract invoice data as strict JSON with keys vendor, date, total, and line_items. "
        "Each line item should include description, quantity, unit_price, and amount when available."
    )

    input_content: List[Dict[str, Any]] = [{"type": "input_text", "text": prompt}]
    if payload["type"] == "text":
        input_content.append({"type": "input_text", "text": payload["data"]})
    else:
        input_content.append(
            {
                "type": "input_image",
                "image_url": f"data:application/octet-stream;base64,{payload['data']}",
            }
        )

    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_MODEL,
            "input": [{"role": "user", "content": input_content}],
            "text": {"format": {"type": "json_object"}},
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text += content.get("text", "")

    return json.loads(text) if text else {}


if __name__ == "__main__":
    import sys

    source = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(extract_invoice_fields(source), indent=2, ensure_ascii=False))
