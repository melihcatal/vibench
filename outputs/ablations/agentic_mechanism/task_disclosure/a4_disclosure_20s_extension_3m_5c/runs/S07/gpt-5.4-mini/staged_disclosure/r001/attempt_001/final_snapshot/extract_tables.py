import base64
import json
import os
from typing import Any, Dict, List, Union

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def _load_document_bytes(source: Union[str, bytes, bytearray]) -> bytes:
    if isinstance(source, (bytes, bytearray)):
        return bytes(source)
    if source.startswith("http://") or source.startswith("https://"):
        response = requests.get(source, timeout=60)
        response.raise_for_status()
        return response.content
    with open(source, "rb") as f:
        return f.read()


def extract_tables(document_source: Union[str, bytes, bytearray]) -> List[Dict[str, Any]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    document_bytes = _load_document_bytes(document_source)
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract all tables from this document. Return JSON only with a top-level key 'tables'. Each table must include rows, and each row must include cells in reading order. Preserve row and cell structure as faithfully as possible.",
                    },
                    {
                        "type": "input_file",
                        "filename": "document",
                        "file_data": base64.b64encode(document_bytes).decode("ascii"),
                    },
                ],
            }
        ],
        "text": {"format": {"type": "json_object"}},
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()

    text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text += content.get("text", "")

    if not text:
        raise RuntimeError("No table extraction output returned")

    parsed = json.loads(text)
    tables = parsed.get("tables", [])
    if not isinstance(tables, list):
        raise RuntimeError("Invalid tables payload")
    return tables


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Extract tables from a document")
    parser.add_argument("document", help="Path or URL to the document")
    args = parser.parse_args()
    print(json.dumps({"tables": extract_tables(args.document)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
