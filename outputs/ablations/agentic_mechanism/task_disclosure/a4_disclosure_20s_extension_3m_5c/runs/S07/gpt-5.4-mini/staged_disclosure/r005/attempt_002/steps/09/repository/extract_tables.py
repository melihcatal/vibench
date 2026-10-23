import os
import json
import base64
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _encode_file(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _build_prompt() -> str:
    return (
        "Extract all tables from the provided document. Return JSON only with this schema: "
        '{"tables":[{"table_index":0,"rows":[{"row_index":0,"cells":[{"cell_index":0,"text":"","row_span":1,"col_span":1}]}]}]}. '
        "Preserve row structure and cell order. If no tables exist, return {\"tables\":[]}."
    )


def extract_tables(document_path: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": _build_prompt()},
                    {
                        "type": "input_file",
                        "filename": os.path.basename(document_path),
                        "file_data": _encode_file(document_path),
                    },
                ],
            }
        ],
        "response_format": {"type": "json_object"},
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text += content.get("text", "")

    if not text:
        return data

    return json.loads(text)


if __name__ == "__main__":
    import sys

    result = extract_tables(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
