import os
import json
import base64
import sys
from urllib import request, error


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _read_input_bytes(path_or_dash: str) -> bytes:
    if path_or_dash == "-":
        return sys.stdin.buffer.read()
    with open(path_or_dash, "rb") as f:
        return f.read()


def _encode_document(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def extract_tables(document_path: str) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    document_bytes = _read_input_bytes(document_path)
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract all tables from the attached document. Return JSON with tables, each table containing row order and cell text. Preserve row and cell structure as accurately as possible.",
                    },
                    {
                        "type": "input_file",
                        "filename": os.path.basename(document_path) if document_path != "-" else "document",
                        "file_data": _encode_document(document_bytes),
                    },
                ],
            }
        ],
        "text": {"format": {"type": "json_object"}},
    }

    req = request.Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=120) as resp:
            response_data = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as e:
        raise RuntimeError(e.read().decode("utf-8", errors="replace")) from e

    output_text = []
    for item in response_data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                output_text.append(content["text"])

    if output_text:
        return json.loads("".join(output_text))
    return response_data


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: extract_tables.py <document-path-or->")
    result = extract_tables(sys.argv[1])
    sys.stdout.write(json.dumps(result, ensure_ascii=False))
